import numpy as np
from .find_interval import find_interval
from .do_tax import do_tax

def MonteCarlo(Config):
    """
    This function runs a Monte Carlo simulation of a personal finance model 
    based on the provided configuration parameters.
    It simulates the financial situation over a specified number of weeks, 
    taking into account income, expenses, savings, and investments.

    Parameters: Config (dict) - A dictionary containing the configuration
                parameters for the simulation.
    Returns: sims (numpy.ndarray) - A 2D array containing the simulation 
             results for each week and iteration.

             mean_vector (numpy.ndarray) - A 1D array containing the mean 
             values of the simulation results across all iterations for each 
             week.

             interval_95 (numpy.ndarray) - A 2D array containing the 95% 
             confidence intervals for the simulation results for each week.

             loan_val (list) - A list containing the value of the loan as it 
             increases yearly
    """

    iterate = Config["iterate"]

    # Balance conditions
    init_balance = Config["init_balance"]    # Initial current account balance
    min_balance = Config["min_balance"]
    max_bal = Config["max_bal"]

    # Savings account conditions
    savings = Config["savings"]    # Value of savings account
    min_save = Config["min_save"]
    apr = Config["apr"]    # apr of said savings account

    # ISA and LISA conditions
    ISA = Config["ISA"]    # Initial value for ISA
    LISA = Config["LISA"]    # Initial value for lifetime ISA
    Ann_LISA_add = Config["Ann_LISA_add"]    # Annual input to the lifetime ISA
    prop_gov_LISA_add = Config["prop_gov_LISA_add"]
    mean_ann_stmkt_return = Config["mean_ann_stmkt_return"]
    sd_ann_stmkt_return = Config["sd_ann_stmkt_return"]

    # Income conditions    
    mean_weekly_income = Config["mean_weekly_income"]
    sd_weekly_income = Config["sd_weekly_income"]

    # Loan conditions
    year_loan = Config["year_loan"]    # yearly maintanence loan
    fee_loan = Config["fee_loan"]    # Student fee loan
    loan_interest = Config["loan_interest"]    # Interest on student loans

    # Weekly spending conditions
    mean_weekly_spend = Config["mean_weekly_spend"]
    sd_weekly_spend = Config["sd_weekly_spend"]
   
    annual_rent = Config["annual_rent"]    # Cost of annual rent

    no_weeks = Config["no_weeks"]   # Number of weeks to simulate

    # Creates a 2D array to store the results of the simulation for each week
    # and iteration
    sims = np.empty((no_weeks, iterate))

    # Creates a list to store the value of the loan as it increases over time
    # In each entry the first value is the loan value the second is the week
    loan_val = [[0, 0]]

    if Config["Placement year"] == False:
        for j in range(52, no_weeks + 1, 52):
            loan_val.append([
                np.round(
                    loan_val[-1][0] - 
                    (
                        ((-1) *
                        loan_interest * 
                        loan_val[-1][0]
                    ) +
                    fee_loan +
                    year_loan
                    ), 
                2),
            j
            ])

        for i in range(iterate):
            
            """
            This is the simulation loop which runs the monte carlo simulation for 
            the number of iterations specified in the Config dictionary.
            """

            # Creates a vector which we can use to store all the weeks of our MC sim for 
            # each pass then use to find mean and confidence intervals
            sim_vector = np.zeros(no_weeks + 1)

            # Sets up all the initial states of the simulation
            balance = [[init_balance, 0]]
            ISA_value = [[ISA, 0]]
            LISA_value = [[LISA, 0]]   
            rent_bills = [[0, 0]]
            saved_money = [[savings, 0]]

            for j in range(1, no_weeks + 1):

                # Work out balance changes for week
                balance.append([
                    (np.round(
                        balance[-1][0] -
                        np.random.normal(
                            mean_weekly_spend,
                            (sd_weekly_spend ** 2)
                        ),
                    2)
                    ),
                    j
                ])
                                                    
                balance.append([
                    np.round(
                        balance[-1][0] + 
                        np.random.normal(
                                mean_weekly_income,
                                (sd_weekly_income ** 2)
                            ),
                        2), 
                    j
                ])

                """
                Every 13 weeks we pay rent and recieve a third of the yearly 
                maintanence loan in the 4th quarter of the year there is no
                maintanence loan payment as the student is expected to be
                working or at home
                """

                if j in range(13, no_weeks + 1, 13):
                    
                    rent_bills.append([annual_rent / 4, j])
                    balance.append([np.round(balance[-1][0] -
                                            rent_bills[-1][0], 
                                            2),
                                    j])

                    if j not in range(52, no_weeks + 1, 52):
                        balance.append([np.round(balance[-1][0] +
                                                year_loan / 3, 
                                                2),
                                        j])

                """
                Once we have dealt with the raw balance changes we make sure to 
                keep our balance and savings above the minimum defined in Config
                as a real student would and ensure our ISA and savings can't go
                negative as in real life
                """

                # Account for taking money from savings
                if balance[-1][0] <= min_balance:
                    take_from_sav = min_balance - balance[-1][0]
                    saved_money.append([saved_money[-1][0] - take_from_sav, j])
                    balance.append([(balance[-1][0] + take_from_sav), j])

                if saved_money[-1][0] <= min_save:
                    take_from_ISA = min_save - saved_money[-1][0]
                    ISA_value.append([ISA_value[-1][0] - take_from_ISA, j])
                    saved_money.append([(saved_money[-1][0] + take_from_ISA), j])

                # ISA and savings both must not go negative
                if ISA_value[-1][0] <= 0:
                    lost_money = 0 - ISA_value[-1][0]
                    ISA_value.append([0, j])
                    saved_money.append([saved_money[-1][0] - lost_money, j])

                    if saved_money[-1][0] <= 0:
                        lost_money = 0 - saved_money[-1][0]
                        saved_money.append([0, j])
                        balance.append([balance[-1][0] - lost_money, j])

                if balance[-1][0] > max_bal:
                    save = balance[-1][0] - max_bal
                    ISA_value.append([ISA_value[-1][0] + save, j])
                    balance.append([balance[-1][0] - save, j])

                # Apply interest
                saved_money.append([np.round(saved_money[-1][0] * 
                                            (1 + apr / 52), 
                                            2),
                                    j])
                ISA_value.append([
                    np.round(
                        ISA_value[-1][0] *
                        (
                        1 + 
                        np.random.normal(
                            mean_ann_stmkt_return, 
                            sd_ann_stmkt_return ** 2
                            ) / 52
                        ),
                    2),
                    j
                ])

                if j in range(52, no_weeks + 1, 52):

                    """
                    Here I'll look at things that don't have balance changed 
                    weekly and are effectively untouched in our time period 
                    """

                    LISA_value.append([np.round(
                                    (LISA_value[-1][0] +
                                    Ann_LISA_add
                                    ) *
                                    (
                                        1 +
                                        prop_gov_LISA_add +
                                        np.random.normal(mean_ann_stmkt_return,
                                                        sd_ann_stmkt_return ** 2
                                                    )
                                    ),
                                    2),
                                j
                            ])

                week_vector = np.zeros(no_weeks + 1)
                week_vector[j] = sum([
                                    ISA_value[-1][0],
                                    LISA_value[-1][0],
                                    balance[-1][0],
                                    saved_money[-1][0],
                                ])

                sim_vector = sim_vector + week_vector

                for n in range(no_weeks):
                    sims[n][i] = sim_vector[n]

        interval_95 = np.empty((2, no_weeks))

        for m in range(no_weeks):
            interval_95[:, m] = np.array(find_interval(0.95, sims[m]))

        mean_vector = (
            (1 / iterate) *
            np.sum(sims, axis=1)
        )
        return sims, mean_vector, interval_95, loan_val

    elif Config["Placement year"] == True:

        p_year_strt_wk = Config["Placement year Start week"]
        p_year_salary = Config["Placement year Salary"]
        p_year_fee_loan = Config["Placement year Fee loan"]
        
        
        for i in range(iterate):
            
            """
            This is the simulation loop which runs the monte carlo simulation for 
            the number of iterations specified in the Config dictionary.
            """

            # Creates a vector which we can use to store all the weeks of our MC sim for 
            # each pass then use to find mean and confidence intervals
            sim_vector = np.zeros(no_weeks + 1)

            # Sets up all the initial states of the simulation
            balance = [[init_balance, 0]]
            ISA_value = [[ISA, 0]]
            LISA_value = [[LISA, 0]]   
            rent_bills = [[0, 0]]
            saved_money = [[savings, 0]]

            for j in range(1, no_weeks + 1):

                if not (j >= p_year_strt_wk and j <= p_year_strt_wk + 52):

                    # Calculate loan interest weekly
                    loan_val.append([
                        np.round(
                            loan_val[-1][0] + 
                            (loan_interest * loan_val[-1][0] / 52),
                        2),
                        j
                    ])

                    # Work out balance changes for week
                    balance.append([
                        (np.round(
                            balance[-1][0] -
                            np.random.normal(
                                mean_weekly_spend,
                                (sd_weekly_spend ** 2)
                            ),
                        2)
                        ),
                        j
                    ])
                                                        
                    balance.append([
                        np.round(
                            balance[-1][0] + 
                            np.random.normal(
                                    mean_weekly_income,
                                    (sd_weekly_income ** 2)
                                ),
                            2), 
                        j
                    ])

                    """
                    Every 13 weeks we pay rent and recieve a third of the yearly 
                    maintanence loan in the 4th quarter of the year there is no
                    maintanence loan payment as the student is expected to be
                    working or at home
                    """

                    if j in range(13, no_weeks + 1, 13):
                        
                        rent_bills.append([annual_rent / 4, j])
                        balance.append([np.round(balance[-1][0] -
                                                rent_bills[-1][0], 
                                                2),
                                        j])

                        if j not in range(52, no_weeks + 1, 52):
                            balance.append([np.round(balance[-1][0] +
                                                    year_loan / 3, 
                                                    2),
                                            j])

                    """
                    Once we have dealt with the raw balance changes we make sure to 
                    keep our balance and savings above the minimum defined in Config
                    as a real student would and ensure our ISA and savings can't go
                    negative as in real life
                    """

                    # Account for taking money from savings
                    if balance[-1][0] <= min_balance:
                        take_from_sav = min_balance - balance[-1][0]
                        saved_money.append([saved_money[-1][0] - take_from_sav, j])
                        balance.append([(balance[-1][0] + take_from_sav), j])

                    if saved_money[-1][0] <= min_save:
                        take_from_ISA = min_save - saved_money[-1][0]
                        ISA_value.append([ISA_value[-1][0] - take_from_ISA, j])
                        saved_money.append([(saved_money[-1][0] + take_from_ISA), j])

                    # ISA and savings both must not go negative
                    if ISA_value[-1][0] <= 0:
                        lost_money = 0 - ISA_value[-1][0]
                        ISA_value.append([0, j])
                        saved_money.append([saved_money[-1][0] - lost_money, j])

                        if saved_money[-1][0] <= 0:
                            lost_money = 0 - saved_money[-1][0]
                            saved_money.append([0, j])
                            balance.append([balance[-1][0] - lost_money, j])

                    if balance[-1][0] > max_bal:
                        save = balance[-1][0] - max_bal
                        ISA_value.append([ISA_value[-1][0] + save, j])
                        balance.append([balance[-1][0] - save, j])

                    # Apply interest
                    saved_money.append([np.round(saved_money[-1][0] * 
                                                (1 + apr / 52), 
                                                2),
                                        j])
                    ISA_value.append([
                        np.round(
                            ISA_value[-1][0] *
                            (
                            1 + 
                            np.random.normal(
                                mean_ann_stmkt_return, 
                                sd_ann_stmkt_return ** 2
                                ) / 52
                            ),
                        2),
                        j
                    ])

                    if j in range(52, no_weeks + 1, 52):
                        """
                        Here I'll look at things that don't have balance changed 
                        weekly and are effectively untouched in our time period 
                        """

                        LISA_value.append([np.round(
                                        (LISA_value[-1][0] +
                                        Ann_LISA_add
                                        ) *
                                        (
                                            1 +

                                            prop_gov_LISA_add +
                                            np.random.normal(mean_ann_stmkt_return,
                                                            sd_ann_stmkt_return ** 2
                                                        )
                                        ),
                                        2),
                                    j
                                ])
                        
                        loan_val.append([
                            np.round(
                                loan_val[-1][0] - 
                                (
                                fee_loan +
                                year_loan
                                ), 
                            2),
                            j
                        ])

                else:
                    # Calculate loan interest weekly
                    loan_val.append([
                        np.round(
                            loan_val[-1][0] + 
                            (loan_interest * loan_val[-1][0] / 52),
                        2),
                        j
                    ])
                    # Work out balance changes for week
                    balance.append([
                        (np.round(
                            balance[-1][0] -
                            np.random.normal(
                                mean_weekly_spend,
                                (sd_weekly_spend ** 2)
                            ),
                        2)
                        ),
                        j
                    ])

                    if j in range(0, p_year_strt_wk + 52, 4):
                        # Pay salary roughly monthly
                        balance.append([np.round(balance[-1][0] +
                                                p_year_salary / 13, 
                                                2),
                                        j])

                    # Still account for rent
                    if j in range(13, no_weeks + 1, 13):
                                            
                        rent_bills.append([annual_rent / 4, j])

                        balance.append([np.round(balance[-1][0] -
                                                rent_bills[-1][0], 
                                                2),
                                        j])

                    # Pay tax mid way through the placement year as an 
                    # approximation of the tax year end
                    if j == p_year_strt_wk + 26:
                        tax_bill = do_tax(p_year_salary)
                        balance.append([np.round(balance[-1][0] -
                                                 tax_bill,
                                                 2),
                                            j])
                                               
                    # Account for taking money from savings
                    if balance[-1][0] <= min_balance:
                        take_from_sav = min_balance - balance[-1][0]
                        saved_money.append([saved_money[-1][0] - take_from_sav, j])
                        balance.append([(balance[-1][0] + take_from_sav), j])

                    if saved_money[-1][0] <= min_save:
                        take_from_ISA = min_save - saved_money[-1][0]
                        ISA_value.append([ISA_value[-1][0] - take_from_ISA, j])
                        saved_money.append([(saved_money[-1][0] + take_from_ISA), j])

                    # ISA and savings both must not go negative
                    if ISA_value[-1][0] <= 0:
                        lost_money = 0 - ISA_value[-1][0]
                        ISA_value.append([0, j])
                        saved_money.append([saved_money[-1][0] - lost_money, j])

                        if saved_money[-1][0] <= 0:
                            lost_money = 0 - saved_money[-1][0]
                            saved_money.append([0, j])
                            balance.append([balance[-1][0] - lost_money, j])

                    if balance[-1][0] > max_bal:
                        save = balance[-1][0] - max_bal
                        ISA_value.append([ISA_value[-1][0] + save, j])
                        balance.append([balance[-1][0] - save, j])

                    # Apply interest
                    saved_money.append([np.round(saved_money[-1][0] * 
                                                (1 + apr / 52), 
                                                2),
                                        j])
                    ISA_value.append([
                        np.round(
                            ISA_value[-1][0] *
                            (
                            1 + 
                            np.random.normal(
                                mean_ann_stmkt_return, 
                                sd_ann_stmkt_return ** 2
                                ) / 52
                            ),
                        2),
                        j
                    ])

                    if j in range(52, no_weeks + 1, 52):
                        """
                        Here I'll look at things that don't have balance changed 
                        weekly and are effectively untouched in our time period 
                        """

                        LISA_value.append([np.round(
                                        (LISA_value[-1][0] +
                                        Ann_LISA_add
                                        ) *
                                        (
                                            1 +

                                            prop_gov_LISA_add +
                                            np.random.normal(mean_ann_stmkt_return,
                                                            sd_ann_stmkt_return ** 2
                                                        )
                                        ),
                                        2),
                                    j
                                ])
                        
                        loan_val.append([
                            np.round(
                                loan_val[-1][0] - 
                                p_year_fee_loan, 
                            2),
                            j
                        ])
        
                week_vector = np.zeros(no_weeks + 1)
                week_vector[j] = sum([
                                    ISA_value[-1][0],
                                    LISA_value[-1][0],
                                    balance[-1][0],
                                    saved_money[-1][0],
                                ])

                sim_vector = sim_vector + week_vector

                for n in range(no_weeks):
                    sims[n][i] = sim_vector[n]

        interval_95 = np.empty((2, no_weeks))

        for m in range(no_weeks):
            interval_95[:, m] = np.array(find_interval(0.95, sims[m]))

        mean_vector = (
            (1 / iterate) *
            np.sum(sims, axis=1)
        )
        return sims, mean_vector, interval_95, loan_val

    else:
        raise ValueError("""Error in config setup. Please check the config dic
        for the following:
        1. Ensure the config settings have the right keys typed correctly

        2. If you have a placement year, please ensure that the start week,
        salary and reduced fee loan are defined in the config dictionary.
        """)