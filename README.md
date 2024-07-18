# Oil Formation Volume Factor Calculator

This is a graphical user interface (GUI) application to calculate the Oil Formation Volume Factor (FVF) based on various equations and input parameters. The application is built using Tkinter for the GUI, and it integrates Matplotlib for plotting the results.

## Features

- Calculate FVF using either the Glaso or Standing equation.
- Load and display CSV data for comparison.
- Visualize FVF versus Pressure with an interactive plot.
- Highlight the bubble point pressure on the plot.

## Installation

1. Ensure you have Python installed (preferably Python 3.6 or later).
2. Install the required libraries using pip:

    ```bash
    pip install numpy matplotlib pandas tk
    ```

3. Download or clone this repository.

## Usage

1. Run the script:

    ```bash
    python oil_fvf_calculator.py
    ```

2. The application window will appear. Fill in the input fields with the required parameters:
   - Bubble Point Pressure (psia)
   - Max Pressure (psia)
   - API Gravity
   - Gas Specific Gravity
   - Temperature (°F)

3. Select the equation for Rs (Solution Gas-Oil Ratio) and Bo (Oil Formation Volume Factor).

4. Click the "Generate Plot" button to calculate and plot the FVF versus Pressure.

5. Optionally, load a CSV file containing pressure and FVF data by clicking "Load CSV Data". Ensure the CSV has columns with the names specified in the input fields for "CSV Pressure Column" and "CSV FVF Column".

## Input Fields

- **Bubble Point Pressure (psia):** The pressure at which gas starts to come out of solution from the oil.
- **Max Pressure (psia):** The maximum pressure for the calculation range.
- **API Gravity:** A measure of how heavy or light the oil is compared to water.
- **Gas Specific Gravity:** The specific gravity of the gas compared to air.
- **Temperature (°F):** The reservoir temperature.
- **Select Bo Equation:** Choose between "Glaso" or "Standing" for the Oil Formation Volume Factor calculation.
- **Select Rs Equation:** Choose between "Glaso" or "Standing" for the Solution Gas-Oil Ratio calculation.
- **CSV Pressure Column:** The name of the pressure column in the CSV file.
- **CSV FVF Column:** The name of the FVF column in the CSV file.

## How It Works

- The application uses the specified equations and input parameters to calculate the FVF at various pressures.
- The results are plotted using Matplotlib.
- If a CSV file is loaded, its data is displayed in a table and plotted alongside the calculated results for comparison.

## Custom Styling

- The application features a custom dark theme using Tkinter's `ttk.Style`.
- The `CustomButton` class provides styled buttons for a consistent look and feel.

## Example

### Input Parameters
- Bubble Point Pressure: 5868 psia
- Max Pressure: 6899 psia
- API Gravity: 42.002
- Gas Specific Gravity: 0.709
- Temperature: 292.1°F

### Sample CSV Structure
| Pressure | FVF |
|----------|-----|
| 5868     | 1.25|
| 5000     | 1.23|
| ...      | ... |

## Contributing

If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
