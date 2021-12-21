import unittest
import sys
import os
sys.path.append(os.getcwd()+"\src")
from DicomFileHandler import DicomHandler as DH


class DicomHandlerTest(unittest.TestCase):
    def setUp(self):
        self.dicomPath = os.getcwd() + "\src\\test\case1.dcm"
        self.niftiPath = os.getcwd() + "\src\\test\case2.nii"
        self.dir = os.getcwd()+ "\src\\test"
    def test_readDicom(self):
        DH.readDicomPydicom( self.dicomPath)

    def test_readDicomNotExist(self):
        self.assertRaises(Exception,DH.readDicomPydicom,self.dir)

    def test_readDicomByte(self):
        DH.readByte(self.dicomPath)


    def test_readDicomByteNotExist(self):
        self.assertRaises(Exception,DH.readByte,self.dir)

    def test_readNifti(self):
        DH.readNifti(self.niftiPath)

    def test_readNiftiNotExist(self):
        self.assertRaises(Exception,DH.readNifti,self.dir)


    def test_writeDicom(self):
        file,name= DH.readDicomPydicom(self.dicomPath)
        DH.writeFilePyDicom(self.dir,name.split("\\")[-1]+"_result",file)


    def test_writeDicomByte(self):
        file,name= DH.readByte(self.dicomPath)
        DH.writeDicomByte(self.dir,name.split("\\")[-1]+"_result",b''.join(file))

if __name__ == '__main__':
    unittest.main()