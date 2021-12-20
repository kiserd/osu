// Author: Donald Logan Kiser
// Date: 01/28/2021
// Description: 


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <fcntl.h>


// global to indicate whether shell is running in foreground-only mode
int FG_ONLY_MODE = 0;


// struct to help organize user input
typedef struct input
{
    char *command;
    int numArgs;
    char *args[513];
    char *argv[514];
    char *inFile;
    char *outFile;
    int bgFlag;
} input;

// struct to keep track of term status of most recently run processes
typedef struct termStatus
{
    int fgStatus;
    int bgStatus;
} termStatus;

// linked list to organize background processes needing term message
typedef struct bgProcess
{
    int pid;
    struct bgProcess *next;
} bgProcess;

char *getInput(void)
/*
DESCRIPTION:    prompts user for command line input and returns
                string to calling function

INPUT:          N/A        

RETURN:         string representation of command line input
*/
{
    // prepare arguments for getline()
    char *inputStr;
    size_t size = 0;
    ssize_t nread;

    // print colon, get user input, return to calling function
    printf(": ");
    nread = getline(&inputStr, &size, stdin);

    // handle case of error **Exploration: Signal Handling API
    if (nread == -1)
    {
        clearerr(stdin);
    }

    // no error, remove newline from user input and return to calling function
    else
    {
        inputStr = strtok(inputStr, "\n");
        return inputStr;
    }
}

char *varExpansion(char *userInputStr)
/*
DESCRIPTION:    replace instances of "$$" with PID

INPUT:          user command line input string

RETURN:         user input string with "$$" replaced
*/
{
    // get PID and make it a string
    pid_t currPid = getpid();
    char *pidString = calloc(30, sizeof(char));
    sprintf(pidString, "%d", currPid);

    // prepare variables and memory for string manipulation
    char *expUserInput = calloc(2049, sizeof(char));
    char *substringPtr;
    int substringSize = strlen("$$");
    int copyStrLen;

    // loop through user input string until strstr() returns null
    while ((substringPtr = strstr(userInputStr, "$$")) != NULL)
    {
        // get length of string leading up to "$$" occurence
        copyStrLen = substringPtr - userInputStr;

        // concatenate string leading up to first occurence to expanded string
        strncat(expUserInput, userInputStr, copyStrLen);

        // concatenate PID string onto expanded user input string
        strcat(expUserInput, pidString);

        // iterate pointers for next round in the loop
        userInputStr = substringPtr + substringSize;
    }
    // handle case where remaining string needs to be added to expanded string
    if (strlen(userInputStr) > 0)
    {
        strcat(expUserInput, userInputStr);
    }
    // free memory and return expanded string to calling function
    free(pidString);
    return expUserInput;
}

int getNumWords(char *expInputStr)
/*
DESCRIPTION:    indicates # of space-delimited words in user input string

INPUT:          user command line input string

RETURN:         integer indication of # of words in input string
*/
{
    // copy user input to string to preserve original
    char *dupInputStr = calloc(strlen(expInputStr), sizeof(char));
    strcpy(dupInputStr, expInputStr);

    // iterate through space-delimited tokens while counting
    int count = 0;
    char *token = strtok(dupInputStr, " ");
    while (token)
    {
        count++;
        token = strtok(NULL, " ");
    }
    
    // free memory and return count to calling function
    free(dupInputStr);
    return count;
}

int inputType(char *currToken)
/*
DESCRIPTION:    returns integer indication of current input type

INPUT:          current token being parsed in user input           

RETURN:         integer indication of input type
*/
{
    // handle case where token indicates end of arguments
    if (currToken == NULL)
    {
        return 0;
    }
    if (strcmp(currToken, "<") == 0)
    {
        return 1;
    }
    if (strcmp(currToken, ">") == 0)
    {
        return 2;
    }
    if (strcmp(currToken, "&") == 0)
    {
        return 3;
    }
    
    // all testing passed, token must be another argument
    return 4;
}

input *parseInput(char *userInputStr, int numWords)
/*
DESCRIPTION:    parses user input string into input struct

INPUT:          user command line input string

RETURN:         pointer to populated input struct
*/
{
    // allocate space for input struct and set numArgs
    input *userInput = calloc(1, sizeof(input));
    userInput->numArgs = 0;

    // duplicate user input string to preserve from strtok_r
    char *dupInputStr = calloc(strlen(userInputStr), sizeof(char));
    strcpy(dupInputStr, userInputStr);

    // iterate through strings in user input and assign to struct properties
    char *token;
    int argCounter = 0;
    int argvIndex = 0;
    int wordCount = 0;
    int inputFlag = 0;
    int outputFlag = 0;
    token = strtok(dupInputStr, " ");
    while (token)
    {
        // get size of token and iterate word count
        int tokenLen = strlen(token);
        wordCount++;
        
        // handle case where token is command
        if (wordCount == 1)
        {
            userInput->command = calloc(strlen(token), sizeof(char));
            strcpy(userInput->command, token);
            userInput->numArgs++;
            userInput->argv[argvIndex] = calloc(strlen(token), sizeof(char));
            strcpy(userInput->argv[argvIndex], token);
            argvIndex++;
        }

        // handle case where token indicates following arg is input file
        else if (strcmp(token, "<") == 0)
        {
            inputFlag = 1;
        }

        // handle case where token indicates following arg is output file
        else if (strcmp(token, ">") == 0)
        {
            outputFlag = 1;
        }

        // handle case where current token is input file
        else if (inputFlag == 1)
        {
            userInput->inFile = calloc(tokenLen, sizeof(char));
            strcpy(userInput->inFile, token);
            inputFlag = 0;
        }

        // handle case where current token is input file
        else if (outputFlag == 1)
        {
            userInput->outFile = calloc(tokenLen, sizeof(char));
            strcpy(userInput->outFile, token);
            outputFlag = 0;
        }

        // handle case where token indicates background process
        else if (strcmp(token, "&") == 0 && wordCount == numWords)
        {
            userInput->bgFlag = 1;;
        }

        // handle case where token is another arg
        else
        {
            userInput->args[argCounter] = calloc(tokenLen, sizeof(char));
            strcpy(userInput->args[argCounter], token);
            argCounter++;
            userInput->numArgs++;
            userInput->argv[argvIndex] = calloc(strlen(token), sizeof(char));
            strcpy(userInput->argv[argvIndex], token);
            argvIndex++;
        }

        // iterate to next token
        token = strtok(NULL, " ");
    }
    // free memory and return populated struct to calling function
    free(dupInputStr);
    return userInput;
}

int notComment(char *userInputStr)
/*
DESCRIPTION:    indicate whether user input represents a comment or blank line

INPUT:          user command line input string

RETURN:         0 represents comment or blank, 1 represents other
*/
{
    // handle case where user input comment
    if (strncmp(userInputStr, "#", 1) == 0)
    {
        return 0;
    }

    // handle case where user input blank line
    if (strlen(userInputStr) == 0)
    {
        return 0;
    }

    // all tests failed, must be something else
    return 1;
}

int commandType(input *userInput)
/*
DESCRIPTION:    gives integer indication of how to handle input

INPUT:          input struct representation of user input

RETURN:         0 represents comment or blank line
                1 represents built-in function
                2 represents function requiring fork() and exec()
*/
{
    // handle case where user input is blank line
    if (!userInput->command)
    {
        return 0;
    }

    // handle case where user input represents comment 
    else if (strncmp(userInput->command, "#", 1) == 0)
    {
        return 0;
    }

    // handle case where command is built in
    else if (strcmp(userInput->command, "status") == 0)
    {
        return 1;
    }
    else if (strcmp(userInput->command, "exit") == 0)
    {
        return 1;
    }
    else if (strcmp(userInput->command, "cd") == 0)
    {
        return 1;
    }

    // handle case where command is NON built-in **requires exec()
    else
    {
        return 2;    
    }
}

void changeDir(input *userInput)
/*
DESCRIPTION:    changes directory to first argument passed

INPUT:          input struct representation of user input

RETURN:         N/A
*/
{
    // define variable to help with chdir() and error communication
    char *dir = malloc(2049 * sizeof(char));
    int success;
    
    // handle case where no additional args are passed
    if (userInput->args[0] == NULL)
    {
        strcpy(dir, getenv("HOME"));
    }

    // handle case where arg is passed
    else
    {
        strcpy(dir, userInput->args[0]);
    }

    // change directory, handle potential error, and free memory
    success = chdir(dir);
    if (success != 0)
    {
        perror("chdir() failed");
    }
    free(dir);
}

void addProcessNode(bgProcess **head, int childPid)
/*
DESCRIPTION:    adds node to the background process tracking linked list

INPUT:          bgProcess struct tracking processes for current program
                and the PID of the process to add

RETURN:         N/A
*/
{
    // prepare new node
    bgProcess *newNode = calloc(1, sizeof(bgProcess));
    newNode->pid = childPid;
    newNode->next = *head;

    // point head to new node
    *head = newNode;
}

void checkProcessNodes(bgProcess **head)
/*
DESCRIPTION:    checks background processes in linked list for termination. If
                process terminated it indicates to the user the termination
                status

INPUT:          bgProcess struct tracking processes for current program

RETURN:         N/A
*/
{
    // initialize and prepare variables for later use
    int childStatus;
    pid_t childPid;
    bgProcess *currNode = *head;
    bgProcess *prevNode;
    bgProcess *tempNode;

    // handle case where linked list is not empty
    if (currNode != NULL)
    {
        // iterate through nodes in LL
        while (currNode != NULL)
        {
            childPid = waitpid(currNode->pid, &childStatus, WNOHANG);
            // handle case where child has NOT terminated
            if (childPid == 0)
            {
                prevNode = currNode;
                currNode = currNode->next;
            }

            // handle case where current child process has terminated;
            else
            {
                // handle case where we need to delete the head
                if (currNode == *head)
                {
                    tempNode = currNode;
                    currNode = currNode->next;
                    free(tempNode);
                    printf("background pid %d is done: exit value %d\n", childPid, childStatus);
                    *head = currNode;
                }
                
                // handle case where we need to delete node other than head
                else
                {
                    tempNode = currNode;
                    prevNode->next = currNode->next;
                    free(tempNode);
                    printf("background pid %d is done: exit value %d\n", childPid, childStatus);
                    currNode = currNode->next;
                }
            }
        }
    }
}

void redirect(input *userInput, int inFlag)
/*
DESCRIPTION:    redirects in/output depending on inFlag variable

INPUT:          input struct representation of user input, file descriptor
                to redirect from/to, binary indication of whether we are
                redirecting input

RETURN:         N/A
*/
{
    // handle case of input redirection
    if (inFlag == 1)
    {
        // handle case where input redirection explicitly ordered
        if (userInput->inFile)
        {
            // get infile file descriptor
            int inFD = open(userInput->inFile, O_RDONLY, 0666);
            if (inFD == -1)
            {
                perror("infile open() failed");
                exit(1);
            }

            // set to close on exec()
            fcntl(inFD, F_SETFD, FD_CLOEXEC);

            // use dup2 to redirect standard input
            int dup2Result = dup2(inFD, 0);
            if (dup2Result == -1)
            {
                perror("infile dup2()");
                exit(1);
            }
        }

        // handle case where background process lacks input redirection
        else if (userInput->bgFlag == 1 && !userInput->inFile)
        {
            // get infile file descriptor
            int inFD = open("/dev/null", O_RDONLY);
            if (inFD == -1)
            {
                perror("infile open() failed on dev/null");
                exit(1);
            }

            // set to close on exec()
            fcntl(inFD, F_SETFD, FD_CLOEXEC);

            // use dup2 to redirect standard input
            int dup2Result = dup2(inFD, 0);
            if (dup2Result == -1)
            {
                perror("infile dup2()");
                exit(1);
            }
        }
    }

    // prepare output redirection
    else if (inFlag == 0)
    {
        // handle case where output redirection explicitly ordered
        if (userInput->outFile)
        {
            // get outfile file descriptor
            int outFD = open(userInput->outFile, O_WRONLY | O_CREAT | O_TRUNC, 0666);
            
            if (outFD == -1)
            {
                perror("outfile open() failed");
                exit(1);
            }

            // set to close on exec()
            fcntl(outFD, F_SETFD, FD_CLOEXEC);

            // use dup2 to redirect standard output
            int dup2Result = dup2(outFD, 1);
            if (dup2Result == -1)
            {
                perror("outfile dup2()");
                exit(1);
            }
        }

        // handle case where background process lacks output redirection
        else if (userInput->bgFlag == 1 && !userInput->outFile)
        {
            // get outfile file descriptor
            int outFD = open("/dev/null", O_WRONLY);
            
            if (outFD == -1)
            {
                perror("outfile open() failed on dev/null");
                exit(1);
            }

            // set to close on exec()
            fcntl(outFD, F_SETFD, FD_CLOEXEC);

            // use dup2 to redirect standard input
            int dup2Result = dup2(outFD, 1);
            if (dup2Result == -1)
            {
                perror("infile dup2()");
                exit(1);
            }
        }
    }
}

void handle_SIGINT(int signo)
/*
DESCRIPTION:    upon receiving SIGINT, check whether foreground process was
                term'd as a result and inform user via stdout

INPUT:          signal number

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // create messages to indicate toggling of foreground-only mode

    char *msg = "terminated by signal 2\n";
    size_t msgSize = 24;

    // indicate to user that child process was term'd
    write(STDOUT_FILENO, msg, msgSize);
}

void customSIGINT(void)
/*
DESCRIPTION:    instructs calling process to note any foreground processes
                that was term'd by a SIGINT signal

INPUT:          N/A

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // initialize sigaction struct
    struct sigaction SIGINT_default = {0};

    // instead of handler function, we use the ignore constant
    SIGINT_default.sa_handler = handle_SIGINT;

    // block all catchable signals
    sigfillset(&SIGINT_default.sa_mask);

    // don't set any flags
    SIGINT_default.sa_flags = SA_RESTART;

    // install handler
    sigaction(SIGINT, &SIGINT_default, NULL);
}

void defaultSIGINT(void)
/*
DESCRIPTION:    instructs calling process to exhibit default behavior upon
                receiving SIGINT

INPUT:          N/A

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // initialize sigaction struct
    struct sigaction SIGINT_custom = {0};

    // instead of handler function, we use the ignore constant
    SIGINT_custom.sa_handler = SIG_DFL;

    // block all catchable signals
    sigfillset(&SIGINT_custom.sa_mask);

    // don't set any flags
    SIGINT_custom.sa_flags = SA_RESTART;

    // install handler
    sigaction(SIGINT, &SIGINT_custom, NULL);
}

void ignoreSIGINT(void)
/*
DESCRIPTION:    instructs calling process to ignore SIGINT

INPUT:          N/A

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // initialize sigaction struct
    struct sigaction SIGINT_ignore = {0};

    // instead of handler function, we use the ignore constant
    SIGINT_ignore.sa_handler = SIG_IGN;

    // block all catchable signals
    sigfillset(&SIGINT_ignore.sa_mask);

    // don't set any flags
    SIGINT_ignore.sa_flags = SA_RESTART;

    // install handler
    sigaction(SIGINT, &SIGINT_ignore, NULL);
}

void handle_SIGTSTP(int signo)
/*
DESCRIPTION:    upon receiving SIGTSTP, flip global variable indicating whether
                shell is running in foreground-only mode or not

INPUT:          signal number

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // create messages to indicate toggling of foreground-only mode
    char *msgFg = "Entering foreground-only mode (& is now ignored)\n";
    size_t msgFgSize = 50;
    char *msgNormal = "Exiting foreground-only mode\n";
    size_t msgNormalSize = 30;

    // handle case where currently running in foreground-only mode
    if (FG_ONLY_MODE == 1)
    {
        write(STDOUT_FILENO, msgNormal, msgNormalSize);
        FG_ONLY_MODE = 0;
    }

    // handle case where currently running in NON foreground-only mode
    else
    {
        write(STDOUT_FILENO, msgFg, msgFgSize);
        FG_ONLY_MODE = 1;
    }
}

void configSIGTSTP(void)
/*
DESCRIPTION:    instructs calling process to ignore SIGTSTP and implement
                custom behavior upon receiving the signal.

INPUT:          N/A

RETURN:         N/A
*/
{
    /*
    the majority of this function was inspired by
    Exploration: Signal Handling API
    */
    // initialize sigaction struct
    struct sigaction SIGTSTP_action = {0};

    // instead of handler function, we use the ignore constant
    SIGTSTP_action.sa_handler = handle_SIGTSTP;

    // block all catchable signals
    sigfillset(&SIGTSTP_action.sa_mask);

    // don't set any flags
    SIGTSTP_action.sa_flags = SA_RESTART;

    // install handler
    sigaction(SIGTSTP, &SIGTSTP_action, NULL);
}

int runCommand(input *userInput, termStatus *stat)
/*
DESCRIPTION:    runs command indicated by input struct as a child process
                via function in the exec() family

INPUT:          input struct representation of user input

RETURN:         integer indication of the new process status
*/
{
    // initialize and prepare variables for later use
    int childStatus;
    pid_t childPid;

    // fork off child process to run command
    pid_t spawnPid = -5;
    spawnPid = fork();
    switch (spawnPid)
    {
        // handle case where fork failed
        case -1 :
            perror("fork() failed!");
            exit(1);
            break;
        
        // handle child process branch
        case 0 :
            // redirect input if applicable
            redirect(userInput, 1);

            // redirect output if applicable
            redirect(userInput, 0);

            // handle case where new process should be run in foreground
            if (userInput->bgFlag == 0 || FG_ONLY_MODE == 1)
            {
                defaultSIGINT();
                execvp(userInput->command, userInput->argv);
            }

            // handle case where new process should be run in background
            else
            {
                execvp(userInput->command, userInput->argv);
            }
            
            // execvp() only returns on error
            perror("execvp");
            exit(1);
            break;

        // handle case of parent process
        default :
            // handle case of foreground process
            if (userInput->bgFlag == 0 || FG_ONLY_MODE == 1)
            {
                customSIGINT();
                childPid = waitpid(spawnPid, &childStatus, 0);
                ignoreSIGINT();

                // decode error message and assign to tracking struct
                if (WIFEXITED(childStatus))
                {
                    stat->fgStatus = WEXITSTATUS(childStatus);
                }
                else
                {
                    stat->fgStatus = WTERMSIG(childStatus);
                }
            }

            // handle case of background process
            else if (userInput->bgFlag == 1)
            {
                printf("background pid is %d\n", spawnPid);
            }
            return spawnPid;
            break;
    }
}

int main(void)
{
    // instruct smallsh process to ignore SIGINT
    ignoreSIGINT();

    // instruct smallsh to exhibit custom behavior upon SIGTSTP
    configSIGTSTP();
    
    // initialize linked list of background process PIDs
    bgProcess *head = NULL;

    // todo
    char *command = calloc(2049, sizeof(char));
    termStatus *stat = calloc(1, sizeof(termStatus));
    do
    {
        // check background processes for potential termination updates
        checkProcessNodes(&head);
        
        // get input from user via command line
        char *inputStr = getInput();

        // expand $$, build input struct, interpret command type
        char *expInputStr = varExpansion(inputStr);
        int numWords = getNumWords(expInputStr);
        input *userInput = parseInput(expInputStr, numWords);
        int commandFlag = commandType(userInput);
        strcpy(command, userInput->command);

        // handle built-in commands
        if (commandFlag == 1)
        {
            // handle case where the user enters cd
            if (strcmp(userInput->command, "cd") == 0)
            {
                changeDir(userInput);
            }

            // handle case where user enters status
            else if (strcmp(userInput->command, "status") == 0)
            {
                printf("exit value %d\n", stat->fgStatus);
            }

            // handle case where user enters exit
            else if (strcmp(userInput->command, "exit") == 0)
            {
                // clean up processes that need term'd
                bgProcess *currNode = head;
                while (currNode)
                {
                    kill(currNode->pid, SIGTERM);
                    printf("background pid %d is done: exit value %d\n", currNode->pid, SIGTERM);
                    currNode = currNode->next;
                    free(head);
                    head = currNode;
                }
            }
        }
        // handle NON built-in commands, requiring fork() and execvp()
        else if (commandFlag == 2)
        {
            // fork process to run command
            int childPid = runCommand(userInput, stat);

            // if background process, add node to linked list
            if (userInput->bgFlag == 1 && FG_ONLY_MODE == 0)
            {
                addProcessNode(&head, childPid);
            }
        }

        // free memory allocated for user input string
        free(inputStr);
        free(expInputStr);
        
        // free memory allocated for user input struct
        free(userInput->command);
        int i = 0;
        while (userInput->args[i])
        {
            free(userInput->args[i]);
            i++;
        }
        i = 0;
        while (userInput->argv[i])
        {
            free(userInput->argv[i]);
            i++;
        }
        free(userInput->inFile);
        free(userInput->outFile);
        free(userInput);
    } while (strcmp(command, "exit") != 0);

    // free memory and exit program
    free(command);
    free(stat);
    exit(0);
}