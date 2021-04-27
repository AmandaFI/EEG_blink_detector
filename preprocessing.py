import os, pickle, csv, copy
from pathlib import Path
import numpy as np
from sklearn.utils import resample
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle



def listFiles(data_folder):
    """Separetes all the files in the folder by their names
    
    Parameters
    ----------
    data_folder : string 
        Path for the folder
    
    Returns
    -------
    list_of_files : list
        All the files in the folder that contain "_data" in the name
    list_of_labels : list
        All the files in the folder that contain "_labels" in the name
    """
    
    list_of_files = [f for f in os.listdir(data_folder) if os.path.isfile(data_folder / f) and '_data' in f]
    list_of_files_labels = [f for f in os.listdir(data_folder) if os.path.isfile(data_folder / f) and '_labels' in f]
    
    return list_of_files, list_of_files_labels

def read_data(path, data_folder, data_files, frequence, limit):
    """Extracts the content of the files and stores in a list
    
    Parameters
    ----------
    path : pathlib
        Path for the data folder
    data_folder : pathlib
        Path for an specific data folder
    data_files : list
        Files type  "_data" from the folder
    frequence : int
        Number indicating the frequence that the data was colect
    limit : int
        Number indicating the amount of lines to be read from the folder
        
    Returns
    -------
    data : list
        Time and readings from EEG contained in the files
    """
    
    data = []

    for file in data_files:
        if data_folder == path / "EEG-IO":
            data.append(np.loadtxt(open(data_folder / file, "rb"), delimiter=";", skiprows=1, usecols=(0,1,2)))
        elif data_folder == path / "EEG-VR" or data_folder == path / "EEG-VV": 
            aux = np.loadtxt(open(data_folder / file, "rb"), delimiter=",", skiprows=5, usecols=(0,1,2))
            aux = aux[0:limit,:]                     
            aux = aux[:,0:3]
            aux[:,0] = np.array(range(0,len(aux)))/frequence  
            data.append(aux)   
    
    return data


def read_labels(data_folder, label_files):
    """Extracts the content of the files and stores in a list 
    
    Parameters
    ----------
    data_folder : pathlib
        Path for an specifc data folder
    label_files : list
       Files type "_labels" from the folder
        
    Returns
    -------
    blinks : numpy.array
        Instants of time indicating the ocurrence of blinks
    corrupt : list
        Corrupted time slots
    """  
    data_folder = Path(data_folder)
    blinks = []
    corrupt = []
    interval_corrupt = []
    n_corrupt = 0
    aux = []
    
    for file in label_files:
        interval_corrupt = []
        with open(data_folder / file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0]=="corrupt":
                    n_corrupt = int(row[1])
                elif n_corrupt > 0:
                    if float(row[1]) == -1:
                        print('Corrupted file: ' + file)
                    else:
                        interval_corrupt.append([float(row[0]), float(row[1])])
                        n_corrupt -= 1
                elif row[0]=="blinks":
                    if n_corrupt != 0:
                        print('Error: ' + file)
                else:
                    aux.append(float(row[0]))
           
        blinks.append(aux)
        corrupt.append(interval_corrupt)
        aux = []
        
    return np.array(blinks, dtype=object), corrupt


def removeCorrupt(rawData, corrupted):
    """Removes corrupt data ranges 
    
    Parameters
    ----------
    rawData : list
        Time and EEG readings 
    corrupted : list
        Ranges of time that contain corrupt data 
        
    Returns
    -------
    cleanData : list
        Data withuot the corrupts ranges  
    """
    
    cont = 0
    aux1 = []
    cleanData = []
    
    for interval in corrupted:
        data = copy.deepcopy(rawData[cont])
        if interval:
            for i in interval:
                for linha in data:
                    if linha[0] < i[0] or linha[0] > i[1]:
                        aux1.append(linha)
                data = aux1
                aux1 = []
            cleanData.append(data)
        else:
            cleanData.append(rawData[cont])
            
        cont+=1
       
    return cleanData

def truncateTime(data):
    """Truncates data according to the precison required 
    
    Parameters
    ----------
    data : list
       Time and EEG readings data 
    
    Returns
    -------
    data : list
        Truncated data 
    """
    
    for group in data:
        for i in range(len(group)):     
            group[i][0] = round(group[i][0],2)
    
    return data    

def movingAverage(data):
    """Calculates the moving average of the data and subtracts from the orginal data
    
    Parameters
    ----------
    data : list
        Time and EEG readings data 
    
    Returns
    -------
    allGroups : list
        Data after process of moving average and subtraction 
    """
    
    allGroups = []
    delta = 200
    
    for group in data:
        aux = np.ones((len(group), len(group[0])))
        aux[:,0] = group[:,0]
        
        c1_0 = np.ones(len(group))
        c2_0 = np.ones(len(group))
        c1 = group[:,1]
        c2 = group[:,2]
        
        for i in range(delta,len(group) - delta):
            c1_0[i] = c1[i-delta:i+delta].sum()/(2*delta)
            c2_0[i] = c2[i-delta:i+delta].sum()/(2*delta)
            
        c1_0[:delta] = c1_0[delta]
        c2_0[:delta] = c2_0[delta]
        c1_0[len(group)-delta:] = c1_0[len(group)-delta-1]
        c2_0[len(group)-delta:] = c2_0[len(group)-delta-1]
        
        c1_0 = c1 - c1_0
        c2_0 = c2 - c2_0
        aux[:,1] = c1_0
        aux[:,2] = c2_0
        
        allGroups.append(aux)
    
    return allGroups

def datasetBlink(delta, data, blinks):
    """Creates a dataset of arrays containing EEG readings corresponding to blink occurances
    
    Parameters
    ----------
    delta : int
        Half of the quantitie of elements in the arrays 
    data : list
        Time and EEG readings data 
    blinks : list
        Instants of time when blink occurred
        
    Returns
    -------
    eegBlink : numpy.array
        Dataset containing EEG readings corresponding to blink occurances
    indexes : list
        Indexes of the elements from the original set that are in the dataset 
    """
       
    quant = 0
    j = 0
    
    for n in blinks:
        quant += len(n)
        
    tam = quant*2            
    eegBlink = np.ones((tam,2*delta))    
    indexes = []
    cont = 0
    
    for group in data:
        ind = []
        aux = []
        for i in range(len(group)):
            if group[i][0] in blinks[j] and group[i][0] not in aux:
                aux.append(group[i][0])
                interval = group[i+1-delta : i+1+delta]                  
                ind = ind + list(range(i+1-delta, i+1+delta,1))
                if len(interval) == 2*delta:
                    eegBlink[cont] = [valor[1] for valor in interval] 
                    eegBlink[cont+1] = [valor[2] for valor in interval] 
                    cont += 2
                    
        indexes.append(ind)         
        j += 1
        
    cut = tuple(range(cont, tam))               
    eegBlink = np.delete(eegBlink, cut, axis=0)
    
    return eegBlink, indexes 

def removeBlink(data, indexes):
    """Removes the elements corresponding to blinks occurances from data 
    
    Parameters
    ----------
    data : list
        Time and EEG readings data 
    indexes : list
        Indexes of elements that will be removed from data 
        
    Returns
    -------
    noBlinkData : list
        Data without blink occurences 
    """
    
    cont = 0
    noBlinkData = []
    
    for group in data:
        noBlink1 = []
        noBlink2 = []
    
        for i in range(len(group)):
            if i not in indexes[cont]:
                noBlink1.append(group[i][1])
                noBlink2.append(group[i][2])
            
        cont += 1
        
        noBlinkData.append(noBlink1)
        noBlinkData.append(noBlink2)
        
    return noBlinkData

def datasetNoBlink(data, tam):
    """Creates a dataset of arrays containing EEG readings without blink occurances
    
    Parameters
    ----------
    data : list
       EEG readings data 
    tam : int
        Number indicating the size of the arrays that the data will be divided 
        
    Returns
    -------
    dividedData : numpy.array
        Group of same sized arrays containing EEG readings without blinking occurences
    """
    dividedData = []
    
    for group in data:
        quant = int(len(group)/tam)
        for i in range(quant):
            dividedData.append(group[i*tam:(i*tam)+tam])
    
    return np.array(dividedData)

