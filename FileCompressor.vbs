Set WshShell = CreateObject("WScript.Shell")

' Check if Python is installed
PythonCheck = WshShell.Run("cmd /c python --version", 0, True)
If PythonCheck <> 0 Then
    MsgBox "Python is not installed! Please install Python from python.org", vbCritical, "FileCompressor Error"
    WScript.Quit
End If

' Install dependencies
WshShell.Run "cmd /c cd backend && python -m pip install -r requirements.txt", 0, True

' Create necessary folders
WshShell.Run "cmd /c mkdir backend\uploads backend\compressed", 0, True

' Start backend server (hidden)
WshShell.Run "cmd /c cd backend && python app.py", 0, False

' Wait for backend to start
WScript.Sleep 3000

' Start frontend server (hidden)
WshShell.Run "cmd /c cd frontend && python -m http.server 8000", 0, False

' Wait for frontend to start
WScript.Sleep 3000

' Open browser
WshShell.Run "http://localhost:8000", 1, False

MsgBox "FileCompressor is now running!" & vbCrLf & vbCrLf & _
       "Web Interface: http://localhost:8000" & vbCrLf & _
       "Backend: http://localhost:5000" & vbCrLf & vbCrLf & _
       "To stop the application, close this message and use Task Manager to kill Python processes.", _
       vbInformation, "FileCompressor Started"