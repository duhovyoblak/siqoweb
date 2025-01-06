#==============================================================================
# SIQO Web server: Initialization of the Project
#------------------------------------------------------------------------------

#==============================================================================
# Windows
#------------------------------------------------------------------------------
pip install -r requirements.txt

pip install D:\GitHub\siqolib
pip install D:\GitHub\siqoweb

#------------------------------------------------------------------------------
# Start siqoweb server in waitress
#------------------------------------------------------------------------------
python D:\GitHub/siqoweb/main.py

#==============================================================================
# Linux DSM
#------------------------------------------------------------------------------
cd /volume1/web/siqoweb

# Ak nie je nainstalovany pip
python -m ensurepip --default-pip

/var/services/homes/Palko/.local/bin/pip3 install -r requirements.txt

cd /volume1/web
/var/services/homes/Palko/.local/bin/pip3 install siqolib
/var/services/homes/Palko/.local/bin/pip3 install siqoweb

cd /volume1/web/siqoweb
python main.py

#------------------------------------------------------------------------------
# Install local siqolib and siqoweb package 
#------------------------------------------------------------------------------
cmd:>pip install D:\GitHub\siqolib
cmd:>pip install D:\GitHub\siqoweb

#==============================================================================
# Start siqoweb server in waitress
#------------------------------------------------------------------------------
python D:\GitHub/siqoweb/main.py

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
