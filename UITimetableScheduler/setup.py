from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

setup(name='TimetableGenerator',
      version='1819.1',
      description='Generate NTU timetable',
      executables=[Executable('userfriendly_timetablescheduler.py', base=None)],
      options={"build_exe": {"packages": ['pandas', 'numpy'],
                             "include_files": ["database.p"]}},
      )
