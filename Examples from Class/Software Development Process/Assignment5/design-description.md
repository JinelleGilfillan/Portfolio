1. When the app is started, the user is presented with the main menu, which allows the user to (1) enter or edit current job details, (2) enter job offers, (3) adjust the comparison settings, or (4) compare job offers (disabled if no job offers were entered yet). <br /><br />

**This requirement is satisfied by the user class with an arrow pointing to the main menu interface, which has a list of options that include entering and editing the current job, enter job offers, adjusting comparison settings, and comparing job offers.** <br /><br />

2. When choosing to enter current job details, a user will:
   1. Be shown a user interface to enter (if it is the first time) or edit all the details of their current job, which consist of:
      1. Title
      2. Company
      3. Location (entered as city and state)
      4. Yearly salary adjusted for cost of living
      5. Yearly bonus adjusted for cost of living
      6. Leave time (in days)
      7. Number of stock option shares offered
      8. Home Buying Program fund (one-time dollar amount up to 15% of Yearly Salary)
      9. Wellness Fund ($0 to $5,000 inclusive annually)
   2. Be able to either save the job details or cancel and exit without saving, returning in both cases to the main menu. <br /><br />

**This requirement is satisfied by the enter/edit current job interface. It has the option to enter job info, save job details, or cancel without saving. When the latter two are selected, there is an arrow indicating that it will take the user back to the main menu.** <br /><br />

3. When choosing to enter job offers, a user will: 
   1. Be shown a user interface to enter all the details of the offer, which are the same ones listed above for the current job.
   2. Be able to either save the job offer details or cancel.
   3. Be able to (1) enter another offer, (2) return to the main menu, or (3) compare the offer (if they saved it) with the current job details (if present). <br /><br />

**This requirement is satisfied by the enter jobs offers interface. The user can enter the job offers from here, they can save the job details, or they can cancel without saving. Once they select save/cancel, there will be three options for them, indicated by the arrow with the black triangle. They can go back to the main menu, they can go back to the enter job offers interface again, or they can go directly to the compare 2 jobs interface.** <br /><br />
  
4. When adjusting the comparison settings, the user can assign integer weights to:
   1. Yearly salary
   2. Yearly bonus
   3. Leave time
   4. Number of shares offered
   5. Home Buying Program Fund
   6. Wellness Fund
   7. If no weights are assigned, all factors are considered equal. <br /><br />

**This requirement is satisfied with the adjust comparison settings interface. The user can enter their comparison weights, then save and return to the main menu. By default, all weights will be equal, until the user has specified their prefered weights.** <br /><br />
 
5. When choosing to compare job offers, a user will:
   1. Be shown a list of job offers, displayed as Title and Company, ranked from best to worst (see below for details), and including the current job (if present), clearly indicated.
   2. Select two jobs to compare and trigger the comparison.
   3. Be shown a table comparing the two jobs, displaying, for each job:
      1. Title
      2. Company
      3. Location
      4. Yearly salary adjusted for cost of living
      5. Yearly bonus adjusted for cost of living
      6. Leave time
      7. Number of shares offered
      8. Home Buying Program fund (one-time up to 15% of Yearly Salary)
      9. Wellness Fund fund ($0 to $5,000 inclusive annually)
   4. Be offered to perform another comparison or go back to the main menu. <br /><br />

**This requirement is satisfied with the compare job offers ranking interface. The default view when entering this interface is a ranked list of job/jjob offers. The current job will be clearly marked. From this interface, the user can select two jobs and compare them by going to the compare 2 jobs interface. From that interface, the user can then select to perform another comparison (the arrow pointing back to the compare job offers ranking), or go back to the main menu (also indicated with an arrow).** <br /><br />

6. When ranking jobs, a job’s score is computed as the weighted sum of:
    ```
    AYS + AYB + (LT * AYS / 260) + (CSO/2) + HBP + WF
    
    where:
    AYS = yearly salary adjusted for cost of living
    AYB = yearly bonus adjusted for cost of living
    LT = leave time
    CSO = Company shares offered (assuming a 2-year vesting schedule and a _ 
              price-per-share of $1)
    HBP = Home Buying Program
    WF= Wellness Fund
   ```
   ```
   For example, if the weights are 2 for the yearly salary, 2 for the 
   yearly bonus, 2 for wellness fund, and 1 for all other factors, 
   the score would be computed as:
    
    
   2/9 * AYS + 2/9 * AYB + 1/9 * (LT * AYS / 260) + 1/9 * (CSO/2) + _ 
          1/9 * HBP + 2/9 * WF
   ```
   <br />

**The is shown in my design as a field on the job type class. It is the only field in the "calculated" property box and it is indicated with a dashed arrow that this property relies on the comparison weights for calculation.** <br /><br />

7. The user interface must be intuitive and responsive. <br /><br />

**This is not shown in my design as it will be fully implemented with the user interface design.** <br /><br />

8. For simplicity, you may assume there is a single system running the app (no communication or saving between devices is necessary). <br /><br />

**This is not shown in my design as the design already assumes a single system.** <br /><br />