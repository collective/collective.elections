# coding="utf-8"
import os, tempfile, sys
from zipfile import ZipFile, ZIP_DEFLATED
import getpass


def getWorkingDirectory():
    """
    returns the full path to a newly created
    temporary working directory
    """
    tmp_dir = tempfile.mkdtemp()
    return tmp_dir

def clearWorkingDirectory(wd):
    """
    removes the temporary working directory
    """
    for file in os.listdir(wd):
        try:
            path = os.path.join(wd, file)
            os.remove(path)
        except OSError:
            pass
    try:
       os.rmdir(wd)
    except:
        pass

def getArchivo(nombreArchivo):
    try:
       archivo_os=open(nombreArchivo,"rb")
       nuevo=archivo_os.read()
       if nuevo:
          return nuevo
    except:
        return None

def zippy(path, archive):
    paths = os.listdir(path)
    for p in paths:
        ruta=p
        p = os.path.join(path, p) # Make the path relative
        if os.path.isdir(p): # Recursive case
            zippy(p, archive)
        else:
            archive.write(p, ruta) # Write the file to the zipfile
    return

def zipit(path, archname):
    # Create a ZipFile Object primed to write
    archive = ZipFile(archname, "w", ZIP_DEFLATED) # "a" to append, "r" to read
    # Recurse or not, depending on what path is
    if os.path.isdir(path):
        zippy(path, archive)
    else:
        archive.write(path)
    archive.close()

def zipeaDirectorio(directorio):
    tmp=getWorkingDirectory()
    salida=os.path.join(tmp, "zipeado.zip")
    zipit(directorio, salida)
    archivo=getArchivo(salida)
    clearWorkingDirectory(tmp)
    return archivo

def copiaArchivo(archivo, salida):
    archivoFuente=archivo
       
    try:               
        archivo_os = open(salida, 'wb')
        archivo_os.write(archivoFuente)
        archivo_os.close()
    except:
        raise

def descifraArchivo(archivo, password):
   archivoFuente=getArchivo(archivo)    
   carpetaTemporal=getWorkingDirectory()
   archivoCifrado=os.path.join(carpetaTemporal, "cifrado")
   archivoAbierto=os.path.join(carpetaTemporal, "abierto")

   copiaArchivo(archivoFuente, archivoCifrado)
   #print 'echo %s|gpg --batch --passphrase-fd 0  --output %s -d %s' % (password, archivoAbierto, archivoCifrado)
   res=os.system('echo %s|gpg --batch --passphrase-fd 0  --output %s -d %s' % (password, archivoAbierto, archivoCifrado))
   if res:
      clearWorkingDirectory(carpetaTemporal)
      raise Exception ("descifrado")
   res= getArchivo(archivoAbierto)
   clearWorkingDirectory(carpetaTemporal)
   return res

def importaLlavePrivada(ruta):
    fin, fout=os.popen4("gpg --import %s" % ruta)
    importacion=fout.read()    
    if importacion.find("clave")< 0:
        return "error"
    return None


def iniciaZipLectura(archivo):
   return ZipFile(archivo, "r", ZIP_DEFLATED) 

def iniciaZipEscritura(archivo):
   return ZipFile(archivo, "w", ZIP_DEFLATED) 

def creaArchivo(name, dir, tipo):
    archivo=os.path.join(dir, name)
    return open(archivo, tipo)

def descomprime(archivoZip, dir):
    tmpDir=getWorkingDirectory()
    zip_os=os.path.join(tmpDir, "zipeado.zip")
    copiaArchivo(archivoZip, zip_os)
    archiveEntrada = iniciaZipLectura(zip_os)    
    names = archiveEntrada.namelist()    
    for name in names:
       temp = creaArchivo(name, dir, "wb")
       datos=archiveEntrada.read(name)
       temp.write(datos)
       temp.close()
    archiveEntrada.close()
    clearWorkingDirectory(tmpDir)
    

def descifraVotos():
    archivoBoletas=raw_input("File with the ballots: ")
    if not(compruebaArchivo(archivoBoletas)):
        print "Files %s does not exist" % archivoBoletas
        return
    archivoSalida=raw_input("Ouput File: ")
    passwd= getpass.getpass("GPG Phrase or password to decipher votes: ")

    archivoZip=None
    try:
       print "Trying to decipher file %s" % archivoBoletas
       archivoZip=descifraArchivo(archivoBoletas, passwd)
       print "File deciphered .............."
    except Exception, inst:
       if ("%s" % inst) !="deciphered":
           print "Error deciphering the file"
       print "Ignoring warning......"
    print ""
    if not(archivoZip):
        archivoZip=getArchivo(archivoBoletas)
    if not(archivoZip):
        print "File with the ballots can not be found"
        return     

    tmpDirDescomprimido=getWorkingDirectory()
    tmpDirDescifrado=getWorkingDirectory()

    try:
       descomprime(archivoZip, tmpDirDescomprimido)
    except:
        print "\nError: can not decompress file %s" % archivoBoletas
        clearWorkingDirectory(tmpDirDescomprimido)
        clearWorkingDirectory(tmpDirDescifrado)        
        return
    
    #descifra cada voto
    for voto in os.listdir(tmpDirDescomprimido):
        votoCifrado=os.path.join(tmpDirDescomprimido, voto)
        votoDescifrado=os.path.join(tmpDirDescifrado, voto)
        try:
           datoDescifrado=descifraArchivo(votoCifrado,passwd)
           copiaArchivo(datoDescifrado,votoDescifrado)
           print "File %s deciphered .....\n" % voto
        except:
            print ""            
            print "Error: Votes could not be decipher. Please Verify"
            return
    try:
       resultado=zipeaDirectorio(tmpDirDescifrado)
    except:
        print "\n Could not compress file with decrypted ballots. " + \
              "compress on Zip the directory %s. " % tmpDirDescifrado
        return
    clearWorkingDirectory(tmpDirDescomprimido)
    clearWorkingDirectory(tmpDirDescifrado)        
    try:
       copiaArchivo(resultado, archivoSalida)
    except:
       print "\nError: Could not get file decryption votes. Please verify"
    print "\nCorrectly decrypted file and put into: '%s'" % archivoSalida
    print "OK"

def firmarDocumento():
    archivo=raw_input("File to sign: ")
    if not(compruebaArchivo(archivo)):
        print "File %s does not exist" % archivo
        return
    archivoSalida=raw_input("Output file: ")
    usuario=raw_input("e-mail of the user that will be used to sign: ")
    passwd= getpass.getpass("GPG Phrase or password to sign file: ")    
    print "Trying signing document"
    salida=os.system("echo %s|gpg --batch --passphrase-fd 0 --output %s -b -a -s -u %s %s" % (passwd, archivoSalida, usuario, archivo))
    if salida:
        print "Error: Could not sign the file %s" % archivo
        return 
    print "File signed"
    
    
def descifrarArchivo():
    archivo=raw_input("File to decrypt: ")
    if not(compruebaArchivo(archivo)):
        print "File %s dont exist" % archivo
        return
    salida=raw_input("Output File: ")
    passwd= getpass.getpass("GPG Phrase or password to decrypt file: ")
    print "Trying decrypt file"
    res=os.system('echo %s|gpg --batch --passphrase-fd 0  --output %s -d %s' % (passwd, salida, archivo))
    if res:
        print "Error: Could not decrypt the file %s" % archivo
        return 
    print "File decrypted"
    
def cifrarArchivo():
    archivo=raw_input("File to encrypt: ")
    if not(compruebaArchivo(archivo)):
        print "File %s dont exist" % archivo
        return
    salida=raw_input("Output File: ")
    usuario=raw_input("e-mail of the user that will be used to sign:: ")
    print "Trying encrypt file"
    res=os.system("gpg --trust-model always --batch -r %s  --output %s --encrypt %s" % (usuario, salida, archivo))
    if res:
        print "Error: Could not encrypt the file %s" % archivo
        return 
    print "File encrypted"    
    
def tieneGPG():
    res=os.system("gpg --version")
    print ""
    print "GPG Found"
    print ""
    print ""
    print ""
    if res:
        return False
    return True

def compruebaArchivo(archivo):
    try:
       tmp= open(archivo, 'r')
       tmp.close()
    except:
       return False
    return True

def exportarLlave():
    mail=raw_input("e-mail of the user for the public key to export: ")
    salida=raw_input("Output File: ")
    print "Trying to export key"    
    res=os.system("gpg --output %s --export -a %s" % (salida, mail))
    if res:
        print "Error: Could not export the public key"
        return 
    print "Public key exported on %s" % salida

def comprobarFirma():
    archivo=raw_input("Original file: ")
    if not(compruebaArchivo(archivo)):
        print "File %s do not exist" % archivo
        return
    firma=raw_input("Signed file: ")
    if not(compruebaArchivo(firma)):
        print "File %s do not exist" % firma
        return

    print "Verifying sign"
    res=os.system("gpg --verify %s %s" % (firma, archivo))
    if res:
        print "Error: Wrong sign"
        return 
    print "Correct Verify"    
    

def generarClaves():
    print "Not yet avaiable"

import time


menu="""
Choose an option

1) Sign a File
2) Encrypt a File
3) Decrypt a File
4) Decrypt votes
5) Export public key
6) Check sign
9) Out

Opcion: """

if __name__=="__main__":
    if not(tieneGPG()):
        print "Error: No se encontro GPG"
        salir= True
    else:
       salir=False
    while not(salir):
        opcion=raw_input(menu)
        if opcion == "1":
            firmarDocumento()
        elif opcion == "2":
            cifrarArchivo()
        elif opcion == "3":
            descifrarArchivo()
        elif opcion =="4":
            descifraVotos()
        elif opcion == "5":
            exportarLlave()
        elif opcion == "6":
            comprobarFirma()
        elif opcion =="9":
            salir=True
            continue
        else:
            print "Opcion no valida"
            time.sleep(2)
            salir=False
            continue
        time.sleep(2)
