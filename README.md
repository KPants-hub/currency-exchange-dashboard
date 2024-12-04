# MGS627
# Currency Exchange Dashboard

## Overview

The **Currency Exchange Dashboard** is a user-friendly web application that provides the latest foreign exchange rates compared to USD Base, as well as historical data visualization for the time period of 2020-03-01 to 03-01-2021. This tool is designed to assist individuals, businesses, and developers in understanding how COVID Impacted currency trends.

---

## Features

- **Latest Exchange Rates**: Get updated currency rates from reliable APIs.
- **Historical Data Charts**: Visualize exchange rate trends over customizable time periods.
- **Favorite Currencies**: Save and prioritize frequently used currencies.
- **Interactive Design**: Functional Drop down to choose the rate the user is interested in.

---

## Technologies Used

- **API Integration**: Exchange rate data from [Fixer.io-API](http://data.fixer.io/api/)
- **Dashboard**: Created using Dash App
- **Libraries**:
  | import requests |
  | import datetime |
  | import pandas |
  | import dash |
  | import plotly|

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/currency-exchange-dashboard.git
   cd currency-exchange-dashboard
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```env
   API_KEY=your_api_key_here
   PORT=5000
   DB_URI=your_mongodb_connection_string
   ```

4. **Run the application**:
   ```bash
   npm start
   ```

5. Open your browser and navigate to `http://localhost:5000`.

---

## Usage

1. **View Exchange Rates**:
   Select base and target currencies to view real-time exchange rates.

2. **Convert Currency**:
   Input an amount in the base currency to see its equivalent in the target currency.

3. **Explore Historical Data**:
   Use the charting tool to track historical exchange rates over days, months, or years.

4. **Save Preferences**:
   Login to save frequently used currencies for quick access.

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to [ExchangeRate-API](https://www.exchangerate-api.com/) for providing the data.
- Inspired by the need for easy and accessible currency exchange tools.

---

## Contact

For questions or feedback, please reach out to [your-email@example.com].

---
