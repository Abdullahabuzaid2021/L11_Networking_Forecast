# L11 Networking Forecast Dashboard

A Streamlit-based dashboard for aggregating and analyzing L11 networking BOM data from Excel files containing PnL SN6600 tabs.

## Features

1. **Automatic File Detection**: Monitors the specified directory for new Excel files
2. **BOM Aggregation**: Automatically aggregates BOM data from all PnL SN6600 tabs across multiple Excel files
3. **Interactive Dashboard**: 
   - Table view with complete BOM summary
   - Bar charts and pie charts for data visualization
   - Key metrics (total items, quantities, files, tabs)
4. **Query Capabilities**:
   - Search by Model/PN or Networking description
   - Filter by quantity ranges
   - Show top N items
5. **Export Functionality**:
   - Export complete summary to Excel
   - Export complete summary to CSV
   - Export query results to CSV
6. **Auto-Refresh**: Optional 30-second auto-refresh for real-time monitoring
7. **Internal Sharing**: Designed for easy sharing within Dell

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run l11_networking_forecast.py
```

## Configuration

- **Default Directory**: `C:\Users\Abdullah_Abuzaid\OneDrive - Dell Technologies\Desktop\Hackathon exercise`
- **Supported File Format**: Excel files (.xlsx) with tabs containing "PnL SN6600" in the name
- **Required Columns**: Networking, Model/PN, Units

## Usage

1. **Load Data**: Click "Load/Refresh Data" to process Excel files
2. **Query Data**: Use the query section to filter and search for specific items
3. **Visualize**: View interactive charts and graphs
4. **Export**: Download results in Excel or CSV format

## Deployment Options for Internal Sharing

### Option 1: Streamlit Cloud (Recommended)
1. Push code to a GitHub repository
2. Connect to Streamlit Cloud (share.streamlit.io)
3. Deploy and share the URL
4. Ensure Excel files are accessible

### Option 2: Internal Server
1. Install on a Dell internal server
2. Run: `streamlit run l11_networking_forecast.py --server.port 8501`
3. Make accessible via VPN/intranet
4. Share the server URL

### Option 3: Local Execution
1. Share the script and requirements.txt
2. Team members run locally
3. Each user needs access to Excel files

## Future Enhancements

- Quarterly forecast analysis
- Delivery schedule parsing
- Trend analysis and forecasting
- Quarter-over-quarter comparisons
- Demand planning metrics
- Authentication and access control

## Technical Details

- **Framework**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **File Processing**: OpenPyXL

## Support

For issues or questions, contact the development team.
