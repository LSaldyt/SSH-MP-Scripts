# Scripts

A collection of basic scripts - mostly for managing an ssh server

To add scripts to PATH:

Append something like:

    # Add custom scripts to path, if they exists  
    echo "Adding Scripts to path"  
    # Add git scripts to path, if they exist  
    if [ -d "$HOME/Scripts/git" ] ; then  
        PATH="$HOME/Scripts/git:$PATH"  
    fi  
    # Add ssh scripts to path, if they exist  
    if [ -d "$HOME/Scripts/ssh" ] ; then  
        PATH="$HOME/Scripts/ssh:$PATH"  
    fi
