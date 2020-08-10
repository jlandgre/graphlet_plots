### Graphlet-Based Time Series Plots Using Seaborn/Matplotlib

This repository contains object-based code for creating "graphlet" based time series plots. These allow stacking multiple categorical and continuous variables into a single plot for visualizing interactions among variables. The example plot and sample Python Jupyter Noteboo code illustrate four types of graphlets based on sample data:
* Categories - Categorical data in a single y-columns
* Multiple Flag Columns - Event "flags" such as (1/0) or (yes/no) in multiple y-columns
* Continuous y variable plotted without rescaling its values
* A rescaled continuous y-variable with specified tick labels in alternate units than the underlying y-axis

<p style="text-align: center;"> Example time-series data
<br/><br/><img src=Assets/Sample_Data.png alt="Sample Data" width=250></p>

<p style="text-align: center;"> <img src=Assets/Plot_example.png alt="Example Graphlet-based Plot" width=800><br/></p>


#### Code Details
The graphlet code is in the Python library file, libs/graphlet_plots.py and is based on Seaborn and Matplotlib. The *.py code is also pasted into initial cells of graphlet.ipynb for ease of debugging. The Jupyter notebook generates the example graphic above. The code takes care of translating original data columns into y-axis units grounded by the first, continuous y-variable's 0 to 100 range. The code uses Python dictionaries to gather needed parameters for each graphlet including its y-axis anchor point, dot color and size, scaling factors and ticklabel dictionary to relate tick y-axis postions to label text. For categorical and flag variables, y-axis translation takes the form of generating spaced y-values from the original categories. For continuous variables, it can save effort to use one continuous, y-variable's (unscaled) data as the y-axis basis for the plot and to then specify scaling factors for other continuous y-variables to translate them into this basis.  These are accompanied by appropriate tick labels to label the plot in each variable's original units. The 0 - 18 hrs tick labels are an example of rescaling.

#### Business, R&D and Manufacturing Data Applications
Graphlet plots are great for visualizing business and technical data and they condense information more naturally than subplots in many cases. One example is showing sales or other financial trends as continuous variables while using flag data points to highlight the onset of marketing events such as promotions, coupons and advertising. A second example is highlighting numerous flag events such as changeovers or reject events related to a manufacturing process.  The time patterns of these can be displayed in concert with continuous variables such as temperatures, pressures and load cell amounts. A third example is visualizing the time course of a consumer research such as a diary study where each usage and its consumer rating are measured by a combination of continuous variables (duration of usage for example) and various product failure modes or flag variables (Used hot water/cold water, Diaper leaked/didn't leak and so on) Plotting these multiple inputs in a graphlet plot is a way to bring out macroscopic trends such as consumers accommodation to the product, failure or flag-variable effects on rating etc.

There are numerous, public examples of such information-rich plots. [Stockcharts.com](https://stockcharts.com/h-sc/ui?s=aapl) is particularly inspirational. Their excellently-designed charts have numerous technical analysis and stock fundamentals endpoints on a single "graphlet" plot.  Their plots also make well-designed use of colors and shading to bring out additional endpoints in stock trends.

#### *Version/Upgrade notes*
8/10/20 - J.D. Landgrebe - Initial Github post of generic code that was basis for a consulting client project
