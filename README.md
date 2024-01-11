Video Link: https://www.youtube.com/watch?v=1Rl_Nbkhp4s

Budget Buddy is a web-based application primarily built using Flask and Python, with the goal of allowing users the freedom to set budget goals and input expenses for any duration. The application offers several key features to enhance user experience: user account authentication, budget goal setting, expense tracking, dashboard overview highlighting a progress bar that indicates the percentage of their budget goal spent.

Instructions to Run Program:
Download the provided budgetbuddy.zip file
Drag budgetbuddy.zip file the into the CS50 codespace
Next, execute the following command: unzip budgetbuddy.zip
Then, you can remove the zip file by executing: rm budgetbuddy.zip and enter “y” when prompted
Then you can change directory into the folder by executing: cd budgetbuddy
Then execute: flask run
Click on the subsequent link to go to our website

In order to use our interface you are first directed to our Login page. However, if you do not have an account you can go to the top right of our navigation bar and click on the tab “Register” to register for an account. Once you click this tab you will be redirected to our Registration page where you will enter your desired username, password, and prompted to re-enter your password for confirmation. If your username, or your password confirmation is wrong you will be redirected to an apology page where it will tell you what went wrong.

Once your account is successfully registered, you will be redirected to your dashboard page. Here you will be greeted with your username, a progress bar, the amount of money you have left for the month and the status of your budget goal. However, as a newly registered user this page will have a pending status. Then, in order to actually set a goal and track your progress you click the Info tab. Here you will see a “Set Goal” portion. You can input your desired goal and once you click the button to set the goal you are redirected to the dashboard page again, where you will see your updated dashboard with the amount of money you have left and your status will show that you are on track. Then in order to add your expenses you can click on the “Info” tab again and scroll down to the “Add Expenses” section. Here you will be prompted to input the type of expense from our dropdown menu, the value, and the name you want to give the expense. Once you click the button, you are once again redirected to the homepage where your dashboard is updated with the corresponding expense amount. For example, if you input an expense of $200, your “money left” on the dashboard will show $200 less and update the progress bar accordingly based on the percentage of the budget you have used. If you were to accidentally input the wrong value, or would like to remove a value, at the bottom of the INFO tab there is a “Remove” section. Here you can view your past history, and the id number associated with your expenses. After locating your expense that you would like to delete you can find the corresponding ID, and enter that into the input box to remove your input and it will update your history of expenses as well as your dashboard.

Now, if you click on the “History” tab you are redirected to a page of our website where you can see your entire expense history. If you click on the “Setting” tab, you will be redirected to a page with a large warning. If you click this button all of your information will be deleted for good. Once you click the button, your dashboard and history will restart.

Once you are done using our application you may go to the upper right hand corner and click the “LogOut” tab where you will be logged out and redirected to the Login page again.
