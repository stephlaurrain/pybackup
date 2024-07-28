import os
import sys
from datetime import datetime
from time import sleep
from utils.mydecorators import _error_decorator
import utils.mylog as mylog
import utils.jsonprms as jsonprms
import utils.file_utils as file_utils
import inspect
import tarfile


class Backup:

    def __init__(self):
        self.root_app = os.getcwd()

    def trace(self, stck):
        self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")

    @_error_decorator()
    def remove_logs(self):
        self.trace(inspect.stack())
        keep_log_time = self.jsprms.prms['keep_log']['time']
        keep_log_unit = self.jsprms.prms['keep_log']['unit']
        self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)   
    
    @_error_decorator()
    def dobackup(self, folder_path, output_filename):
        with tarfile.open(output_filename, "w:gz") as tar:
            # Ajoute le dossier à l'archive tar.gz
            tar.add(folder_path, arcname=os.path.basename(folder_path))

    @_error_decorator()
    def main(self):
    
        self.log = mylog.Log()
        self.log.init("default")
        self.trace(inspect.stack())
        # params
        nbargs = len(sys.argv)
        command = "test" if (nbargs == 1) else sys.argv[1]
        # fichier json en param
        jsonfile = "default" if (nbargs < 3) else sys.argv[2].lower()
        print("params=", command, jsonfile, )

        # json
        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
        self.jsprms = jsonprms.Prms(jsonFn)
        self.remove_logs()

        if command == "backup":
            dirs_to_save = self.jsprms.prms["to_save"]
            today = datetime.now()
            dnow = today.strftime(r"%y%m%d%H%M") 
            for dir in dirs_to_save:
                print(dir['name'])
                print(f"{dir['destdir']}{os.path.sep}{dir['name']}-{dnow}.tar.gz")
                self.dobackup(dir['startdir'], f"{dir['destdir']}{os.path.sep}{dir['name']}-{dnow}.tar.gz")
   
   

        self.log.lg("=THE END COMPLETE=")