import os
for folder in ["bank_dadar","bank_mahim","municipal","uidai"]:
    os.chdir(folder)
    try:
        os.remove(folder+".sqlite")
    except Exception as e:
        pass
    os.system("python3 set_up_db.py")
    os.chdir("..")
