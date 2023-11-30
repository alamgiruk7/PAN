@ECHO OFF
:: This batch file try to provide similar functionality to the windows users to run the project
:: in Dev mode as provided to LINUX/UNIX users in the relevant (runDebug.sh) file.
:: Dev server config vars are set here.

SET FLASK_APP=app
SET FLASK_ENV=development
SET SECRET_KEY=5a81d9afb1c40f95106e1aa4b2f487a77f5e71f1e7992c693c714108649e21dc8ea465a9b8f32bdf624f06d3be4ec33383e69e0dd0125247073964a6c29256524f2ae7baff98a83e500fab01310aa4c04201744ecbb8485d475b360f2d43e6ad4d1d896906fdc4eb6cc3c0f2c9da7711503be671ae22071f5dac6f40e04ff823

:: Local DB config vars are set here
SET DB_HOST=localhost
SET DB_PORT=27017
@REM SET DB_USER=postgres
@REM SET DB_PW=root
SET DB_NAME=pan

:: Development DB config vars are set here


:: Test DB config vars are set here


:: Production DB config vars are set here


CMD /k "python runApp.py"