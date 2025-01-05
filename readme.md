
#==============================================================================
# SIQO Web server: Initialization of the Project
#------------------------------------------------------------------------------

#==============================================================================
# environment setup
#------------------------------------------------------------------------------
cmd:>pip install -r requirements.txt

#------------------------------------------------------------------------------
# Install local siqolib and siqoweb package 
#------------------------------------------------------------------------------
cmd:>pip install D:\GitHub\siqolib
cmd:>pip install D:\GitHub\siqoweb

#==============================================================================
# Start siqoweb server in waitress
#------------------------------------------------------------------------------
waitress-serve --host 127.0.0.1 --port 8082  --threads 100 __init__:app

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
