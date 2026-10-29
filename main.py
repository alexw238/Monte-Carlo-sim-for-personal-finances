import numpy as np
from Classes.FEQ import FEQ 

# Define our start conditions

iterate = 10000

# Cash inflow in £s
ISA = 10000    # Initial value for ISA
LISA = 0    # Initial value for lifetime ISA
Ann_LISA_add = 4000    # Annual addition to the lifetime ISA
prop_gov_LISA_add = 0.25
savings = 2000    # Value of savings account
apr = 0.05    # apr of said savings account
weekly_income = 80
year_loan = 5000    # yearly maintanence loan
mean_ann_stmkt_return = 0.1
sd_ann_stmkt_return = 0.13
init_balance = 2000    # Initial current account balance

# Cash outflow in £s
fee_loan = 9500    # Student fee loan
mean_weekly_spend = 200
sd_weekly_spend = 8
annual_rent = 10500    # Cost of annual rent
loan_interest = 0.05    # Interest on student loans

no_weeks = 156 # Number of weeks to simulate

##############################################################################
# main - time unit is weeks                                                  #
##############################################################################

np.random.seed(28907314)

# Creates list for all the outputs of the monte carlo sim
potential_money = []


for i in range(iterate):

    # Sets up initial future events queue to be added to must be setup fresh
    # for each simulation because feq_i is not reset with each loop
    feq_i = FEQ([[ISA +
                    LISA +
                    savings +
                    init_balance, 0]])

    # Sets up all the lists of event's in the right format
    week_spends = [[0, 0]]
    week_in = [[0, 0]]
    ISA_changes = [[0, 0]]
    ISA_value = [ISA]    # Keeps track of ISA value
    LISA_changes = [[0, 0]]
    LISA_value = [LISA]    # Keeps track of LISA value
    rent_bills = [[0, 0]]
    saved_money = [[0, 0]]
    loan_take_out = [[0, 0]] # Money in from taking out a loan
    loan_fees = [[(-1) * (fee_loan + year_loan), 0]]
    loan_value = [0]    # Keeps track of loan value

    for j in range(1, no_weeks + 1):
        ######################################################################
        # Calculates weekly in and outflow and makes events for them         #
        ######################################################################

        week_spends.append([((-1) * np.random.normal(mean_weekly_spend,
                                            (sd_weekly_spend ** 2)
                                            )),
                                            j]
                                            )
        
        week_in.append([weekly_income, j])

    for j in range(13, no_weeks + 1, 13):
        ######################################################################
        # Calculates everything that is factored in quarterly and makes an   #
        # Event for each quarter                                             #
        ######################################################################
        
        # Find new ISA total from changes
        ISA_value.append(ISA_value[-1] + ISA_changes[-1][0])

        # add the change in ISA value to the FEQ to track gain / loss
        ISA_changes.append([(np.random.normal(mean_ann_stmkt_return,
                                            (sd_ann_stmkt_return ** 2) /
                            4)) *
                            ISA_value[-1],
                            j]
                            )

        # Same process as ISA values
        LISA_value.append(LISA_value[-1] + LISA_changes[-1][0])
        
        LISA_changes.append([(prop_gov_LISA_add + 
                                np.random.normal(mean_ann_stmkt_return,
                                            (sd_ann_stmkt_return ** 2)) /
                                4) *
                            LISA_value[-1] +
                            Ann_LISA_add / 4,
                            j]
                            )

        rent_bills.append([(-1) * annual_rent / 4, j])

        saved_money.append([savings * (1 + (apr / 4)), j])

        loan_take_out.append([year_loan / 4, j])

    for j in range(52, no_weeks + 1, 52):

        # Similar to ISAs tracks current loan value for interest purposes
        loan_value.append(loan_value[-1] + 
                          (-1) * loan_fees[-1][0] 
        )
        
        # Calculates loan_fees yearly and makes an event for each change
        loan_fees.append([(-1) *
                          (
                          loan_interest * 
                          loan_value[-1] +
                          fee_loan +
                          year_loan
                          ),
                          j])
    
    # Adds all the events we just created to our queue
    feq_i = feq_i.add_list(week_spends)
    feq_i = feq_i.add_list(saved_money)
    feq_i = feq_i.add_list(week_in)
    feq_i = feq_i.add_list(ISA_changes)
    feq_i = feq_i.add_list(LISA_changes)
    feq_i = feq_i.add_list(rent_bills)
    feq_i = feq_i.add_list(loan_take_out)
    feq_i = feq_i.add_list(loan_fees)

    # Gets initial value for total money
    money = 0

    # Calculates money after each event happens leaving a final total
    for event in feq_i.FEQ:
        money = money + feq_i.FEQ[0][0]
        feq_i = feq_i.GoToNext()[0]
    
    potential_money.append(money)

print(max(potential_money), min(potential_money), np.mean(potential_money))