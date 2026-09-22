# L11 Networking Forecast Dashboard

A Streamlit-based dashboard for aggregating and analyzing L11 networking BOM data from Excel files containing PnL SN6600 tabs.

## 🚀 Quick Access

**Dashboard URL**: http://localhost:8501 (when running locally)

**GitHub Repository**: https://github.com/Abdullahabuzaid2021/L11_Networking_Forecast

**SharePoint Data Source**: [Hackathon - L11 forecasting](https://dell.sharepoint.com/:f:/r/sites/NetworkingL11RackPlanning/Shared%20Documents/General/Hackathon%20-%20L11%20forecasting?d=wb9ae5c4571d84bec94d375ef7ea58856&csf=1&web=1&e=KNnpRl)

## Problem Statement

The L11 networking team faces a significant challenge in aggregating Bill of Materials (BOM) data from multiple individual project files. Each project maintains its own Excel file with networking component data in PnL SN6600 tabs, making it difficult to:

- **Consolidate Data**: Aggregate quantities across multiple projects to get total networking requirements
- **Ensure Data Accuracy**: Validate that data from different sources is consistent and usable before analysis
- **Real-time Monitoring**: Track changes and new additions across multiple project files
- **Strategic Planning**: Make informed decisions based on comprehensive networking component forecasts

The manual process of combining data from numerous Excel files is time-consuming, error-prone, and doesn't provide the real-time visibility needed for effective planning and forecasting.

## Plan Function

To address these challenges, we developed an automated solution with the following approach:

1. **Automated Data Aggregation**: Create a system that automatically processes all Excel files in a designated directory
2. **Data Validation**: Implement robust data validation to ensure accuracy and consistency before use
3. **Interactive Dashboard**: Build a user-friendly interface for querying, visualizing, and exporting the aggregated data
4. **Real-time Updates**: Enable automatic detection of new files and data refresh capabilities
5. **Internal Collaboration**: Design the system for easy sharing within Dell's internal environment

## Solution Steps Breakdown

### Phase 1: Data Processing Engine
- **File Detection**: Implemented automatic scanning of directories for Excel files with PnL SN6600 tabs
- **Data Extraction**: Created robust parsing logic to handle varying Excel file structures
- **Data Validation**: Added validation to ensure data accuracy:
  - Required column checks (Model/PN, Units)
  - Optional column handling (Networking)
  - Zero-value filtering
  - Section detection to exclude pricing/summary tables
- **Data Aggregation**: Developed logic to combine data from multiple files and sum quantities by Model/PN

### Phase 2: Dashboard Development
- **User Interface**: Built Streamlit-based dashboard with intuitive navigation
- **Data Visualization**: Implemented interactive charts (bar charts, pie charts) for data analysis
- **Query Capabilities**: Added search and filtering functionality for specific item analysis
- **Export Features**: Enabled Excel and CSV export for reporting and sharing

### Phase 3: Advanced Features
- **Project File Breakdown**: Created pivot matrix showing quantities per project file
- **Quantity Analysis**: Added statistical analysis (min, max, median, standard deviation)
- **New File Detection**: Implemented visual indicators for new files added to the directory
- **Auto-Refresh**: Added optional automatic data refresh functionality

### Phase 4: Deployment & Sharing
- **Internal Sharing**: Configured for Dell internal network access
- **Source Control**: Managed code through GitHub for collaboration
- **Documentation**: Created comprehensive setup and usage documentation
- **Scalability**: Designed for easy deployment on Streamlit Cloud or internal servers

## Conclusion of Outcome

The L11 Networking Forecast Dashboard successfully addresses the original problem statement by providing:

### ✅ Key Achievements
- **Automated Aggregation**: Processes multiple Excel files automatically, eliminating manual consolidation
- **Data Accuracy**: Implements robust validation to ensure only accurate, usable data is included
- **Real-time Visibility**: Provides immediate visibility into total networking requirements across all projects
- **Interactive Analysis**: Enables detailed querying and filtering of component data
- **Strategic Insights**: Supports better planning through comprehensive data visualization and export capabilities

### 📊 Measurable Results
- **Processing Efficiency**: Reduces data consolidation time from hours to seconds
- **Data Accuracy**: Eliminates manual errors through automated validation
- **Coverage**: Successfully processes diverse Excel file structures with flexible column handling
- **User Adoption**: Intuitive interface enables quick adoption by team members
- **Scalability**: Designed to handle growing numbers of projects and files

### 🎯 Business Impact
- **Improved Planning**: Better forecasting accuracy for networking component requirements
- **Cost Optimization**: Enhanced visibility enables better procurement decisions
- **Time Savings**: Significant reduction in manual data processing time
- **Error Reduction**: Automated validation eliminates manual consolidation errors
- **Collaboration**: Enables team-wide access to consistent, up-to-date BOM data

The dashboard has transformed a manual, error-prone process into an automated, reliable system that provides real-time insights for L11 networking planning and decision-making.

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

## Dashboard Access

### Local Development
When running locally, the dashboard is accessible at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://10.137.51.248:8501 (within Dell network)
- **External URL**: http://143.166.192.16:8501 (if accessible)

### Deployment Options
The dashboard can be deployed for team access through:

**Streamlit Cloud** (Recommended for sharing):
- Deploy via GitHub integration
- Get a permanent URL like `https://l11-networking-forecast.streamlit.app`
- Easy sharing with team members

**Internal Server**:
- Deploy on Dell internal servers
- Configure for intranet access
- Suitable for sensitive data

### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run l11_networking_forecast.py`
4. Access at http://localhost:8501
5. Click "Load/Refresh Data" to process the included sample files

## Configuration

- **Default Directory**: `data/` (included in repository with sample files)
- **Alternative Directory**: `C:\Users\Abdullah_Abuzaid\OneDrive - Dell Technologies\Desktop\Hackathon exercise`
- **SharePoint Location**: [Hackathon - L11 forecasting](https://dell.sharepoint.com/:f:/r/sites/NetworkingL11RackPlanning/Shared%20Documents/General/Hackathon%20-%20L11%20forecasting?d=wb9ae5c4571d84bec94d375ef7ea58856&csf=1&web=1&e=KNnpRl)
- **Supported File Format**: Excel files (.xlsx) with tabs containing "PnL SN6600" in the name
- **Required Columns**: Networking, Model/PN, Units
- **Dashboard URL**: http://localhost:8501 (when running locally)

### Sample Data Included

The repository includes sample Excel files in the `data/` directory:
- `Horizon PNL.xlsx` - Sample Horizon project BOM data
- `P&L -IREN - 50MW 252 Racks - Sweetwater VR NVL72_SN6600-LD_CORE.xlsx` - CORE project data
- `P&L -IREN - 50MW 252 Racks - Sweetwater VR NVL72_SN6600-LD_DH.xlsx` - DH project data

These files can be used immediately to test the dashboard functionality.

### Data Directory Structure

```
L11_Networking_Forecast/
├── data/
│   ├── Horizon PNL.xlsx
│   ├── P&L -IREN - 50MW 252 Racks - Sweetwater VR NVL72_SN6600-LD_CORE.xlsx
│   └── P&L -IREN - 50MW 252 Racks - Sweetwater VR NVL72_SN6600-LD_DH.xlsx
├── l11_networking_forecast.py
├── requirements.txt
└── README.md
```

### SharePoint Integration

The dashboard is designed to work with locally synced SharePoint folders. To use the SharePoint location:

1. **Sync SharePoint Folder**: Use OneDrive or SharePoint sync client to sync the folder locally
2. **Use Local Path**: Configure the dashboard to use the local synced folder path
3. **Automatic Updates**: Changes in SharePoint will sync to the local folder and be detected by the dashboard

**Note**: Direct SharePoint API integration requires additional authentication setup. The current implementation uses local file system access for simplicity and security.

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

## 📱 Dashboard Links

### Local Access
- **Primary URL**: http://localhost:8501
- **Network URL**: http://10.137.51.248:8501 (Dell internal network)
- **External URL**: http://143.166.192.16:8501 (if accessible)

### Repository & Resources
- **GitHub Repository**: https://github.com/Abdullahabuzaid2021/L11_Networking_Forecast
- **SharePoint Data**: [Hackathon - L11 forecasting](https://dell.sharepoint.com/:f:/r/sites/NetworkingL11RackPlanning/Shared%20Documents/General/Hackathon%20-%20L11%20forecasting?d=wb9ae5c4571d84bec94d375ef7ea58856&csf=1&web=1&e=KNnpRl)

### Quick Start Commands
```bash
# Clone the repository
git clone https://github.com/Abdullahabuzaid2021/L11_Networking_Forecast.git
cd L11_Networking_Forecast

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run l11_networking_forecast.py

# Access the dashboard
# Open http://localhost:8501 in your browser
```
