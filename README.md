# Monte Carlo Personal Finance Simulator

A Python-based Monte Carlo simulation tool designed to model personal financial trajectories, and student debt over the next few years. 

The simulator allows you to compare your financial situation with versus without taking a professional placement year.

## Features
* **Scenario Comparison:** Directly models and plots your projected net worth and student debt with vs. without a placement year.
* **Volatility Modelling:** Simulates market fluctuations and variable lifestyle expenses using independent Gaussian distributions.
* **Taxation & Market Variance:** Accounts for basic tax variability only on placement year salary.

## Prerequisites
The simulator requires Python 3.0+ and the following dependencies:
* **Python** (Tested on version 3.15.2)
* **NumPy** (Tested on version 2.5.4)
* **Matplotlib** (Tested on version 3.11.2, utilizes `pyplot` and `GridSpec`)

## Installation
1. Download the project repository as a `.zip` archive.
2. Extract the contents to your preferred working directory.
3. Open your terminal, navigate to the project folder, and install dependencies if missing:
   ```bash
   pip install numpy matplotlib
   ```

## Usage
1. Open `main.py` in your preferred text editor or IDE.
2. Navigate to the `Config` class/dictionary structure at the top of the file.
3. Adjust the variables to match your situation, following the guidelines in the inline comments.
4. Run the simulation:
   ```bash
   python main.py
   ```

## Limitations
1. Doesn't account for potential disastrous circumstances (e.g financial crises, or breaking a phone or laptop and needing to buy a new one)
2. All random events are assumed to be independent and Gaussian distributed this is not completely realistic but I believe sufficient for the models aims
3. Relatively slow I haven't made explicit attempts to optimise the code and so it is only able to model a few 1000 iterations per second even on my fairly powerful machine
4. Low resolution some events happen on a daily scale or mid way through a week or month which this model will fail to simulate as it operates on a week by week basis

## License
This is free and unencumbered software released into the public domain under **The Unlicense**. 

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means. For more information, please refer to <https://unlicense.org>.

## Credits
* **Developer:** Alexander Woolliams
* **Core Packages:** Python, NumPy, Matplotlib