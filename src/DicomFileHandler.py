import pydicom
import nibabel as nib
from nibabel.testing import data_path
import os
import Type as TP


class DicomFileHandler:

    def readByte(self, name):
        try:
            result = []
            with open(name, "rb") as f:
                byte = f.read(1)
                while byte:
                    result.append(byte)
                    byte = f.read(1)
            return result, self.getNameOfFile(name)
        except Exception  as e:
            raise Exception('wrogn path')


    def writeDicomByte(self, path, name, byteArray):
        with open(self.createDcmName(path, name), "wb") as f:
            f.write(byteArray)

    def readNifti(self, name):
        try:
            filePath = os.path.join(data_path, name)
            return nib.load(filePath), self.getNameOfFile(name)
        except:
            raise Exception("wrong path")

    def readDicomPydicom(self, name):
        try:
            file = pydicom.dcmread(name)
            return file, self.getNameOfFile(name)
        except:
            raise Exception('wrogn path')

    def writeFilePyDicom(self, path, name, result):
                result.save_as(self.createDcmName(path, name))

    def getNameOfFile(self, name):
        return name.split('/')[-1].split('.')[0] + "_result"

    def getFileType(self, name):
        stringType = self.getFileTypeName(name)
        if (stringType == "dcm"):
            return TP.Type.DICOM
        elif (stringType == "nii"):
            return TP.Type.NIFTI
        else:
            raise Exception("the app dose not support this kind of format")

    def getFileTypeName(self, name):
        return name.split('/')[-1].split('.')[1]

    def createDcmName(self, path, name):
        return path + "/" + name + ".dcm"


DicomHandler = DicomFileHandler()
