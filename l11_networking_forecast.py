import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time
from datetime import datetime
import os
import io

# Page configuration
st.set_page_config(
    page_title="L11 Networking Forecast",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0076CE;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .dell-blue {
        color: #0076CE;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🌐 L11 Networking Forecast Dashboard</h1>', unsafe_allow_html=True)
st.markdown("""
This dashboard provides L11 networking BOM forecasting and analysis. It automatically aggregates data from Excel files
containing PnL SN6600 tabs and provides interactive querying and export capabilities.
""")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# Directory input
default_dir = r"C:\Users\Abdullah_Abuzaid\OneDrive - Dell Technologies\Desktop\Hackathon exercise"
sharepoint_url = "https://dell.sharepoint.com/:f:/r/sites/NetworkingL11RackPlanning/Shared%20Documents/General/Hackathon%20-%20L11%20forecasting?d=wb9ae5c4571d84bec94d375ef7ea58856&csf=1&web=1&e=KNnpRl"

excel_directory = st.sidebar.text_input("Excel Directory", default_dir)
st.sidebar.caption("💡 For SharePoint access, sync the folder locally or use the mapped drive path")

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("Auto-refresh (30 seconds)", value=False)

# Function to process Excel files and aggregate BOM data
def process_bom_data(directory):
    """Process all Excel files and aggregate BOM data from PnL SN6600 tabs"""
    all_data = []
    file_info = []
    
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return None, None, "Directory not found"
        
        # Iterate through all Excel files in the directory
        for file_path in dir_path.glob('*.xlsx'):
            file_name = file_path.name
            file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            # Load the Excel file
            try:
                xl = pd.ExcelFile(file_path)
                
                # Find tabs that include "PnL SN6600" in their name
                pnl_tabs = [sheet for sheet in xl.sheet_names if 'PnL SN6600' in sheet]
                
                for tab_name in pnl_tabs:
                    # Read the tab with no header to find the header row
                    df = pd.read_excel(file_path, sheet_name=tab_name, header=None)
                    
                    # Find the header row (row containing 'Model/PN')
                    header_row = None
                    for idx, row in df.iterrows():
                        if 'Model/PN' in row.values:
                            header_row = idx
                            break
                    
                    if header_row is not None:
                        # Read the data with the correct header
                        df = pd.read_excel(file_path, sheet_name=tab_name, header=header_row)
                        
                        # Extract relevant columns
                        if 'Model/PN' in df.columns and 'Units' in df.columns:
                            # Add source file and tab information
                            df['Source File'] = file_name
                            df['Source Tab'] = tab_name
                            df['File Modified'] = file_modified
                            
                            # Add Networking column if it doesn't exist
                            if 'Networking' not in df.columns:
                                df['Networking'] = 'N/A'
                            
                            # Select only the columns we need
                            relevant_data = df[['Networking', 'Model/PN', 'Units', 'Source File', 'Source Tab', 'File Modified']].copy()
                            
                            # Remove rows where Model/PN is NaN
                            relevant_data = relevant_data[relevant_data['Model/PN'].notna()]
                            
                            # Convert Units to numeric, coerce errors to NaN
                            relevant_data['Units'] = pd.to_numeric(relevant_data['Units'], errors='coerce')
                            
                            # Remove rows where Units is NaN or 0
                            relevant_data = relevant_data[relevant_data['Units'].notna()]
                            relevant_data = relevant_data[relevant_data['Units'] != 0]
                            
                            # Filter out summary/pricing sections by detecting patterns
                            # Look for rows that might be summary sections rather than item data
                            summary_keywords = ['Total Data Hall', 'Total Core', 'Total Horizon', 'Data Hall E-W', 'Data Hall N-S', 'Data Hall OOB', 'Core E-W', 'Core N-S', 'Core OOB', 'Rack Integration']
                            
                            # Filter out rows where Model/PN exactly matches summary section names
                            relevant_data = relevant_data[
                                ~relevant_data['Model/PN'].isin(summary_keywords)
                            ]
                            
                            # Filter out rows where Model/PN starts with "Total" (but not "Total" as part of a real model number)
                            relevant_data = relevant_data[
                                ~relevant_data['Model/PN'].str.startswith('Total ', na=False)
                            ]
                            
                            all_data.append(relevant_data)
                            file_info.append({
                                'File': file_name,
                                'Tab': tab_name,
                                'Items': len(relevant_data),
                                'Modified': file_modified
                            })
            
            except Exception as e:
                st.error(f"Error processing {file_name}: {e}")
                continue
        
        if all_data:
            # Combine all data
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Aggregate by Model/PN - sum the Units and get the Networking value
            summary_df = combined_df.groupby('Model/PN').agg({
                'Networking': 'first',
                'Units': 'sum'
            }).reset_index()
            
            # Filter out items with total Units = 0
            summary_df = summary_df[summary_df['Units'] != 0]
            
            # Sort by Units descending
            summary_df = summary_df.sort_values('Units', ascending=False)
            
            # Reorder columns: Networking, Model/PN, Units
            summary_df = summary_df[['Networking', 'Model/PN', 'Units']]
            
            # Ensure proper data types
            summary_df['Model/PN'] = summary_df['Model/PN'].astype(str)
            summary_df['Networking'] = summary_df['Networking'].astype(str)
            
            # Create file info dataframe
            files_df = pd.DataFrame(file_info)
            
            # Ensure proper data types for combined data
            combined_df['Model/PN'] = combined_df['Model/PN'].astype(str)
            combined_df['Networking'] = combined_df['Networking'].astype(str)
            combined_df['Source File'] = combined_df['Source File'].astype(str)
            
            return summary_df, files_df, combined_df, None
        else:
            return None, None, None, "No PnL SN6600 tabs found in any files"
            
    except Exception as e:
        return None, None, None, f"Error processing data: {str(e)}"

# Main content area
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📁 Data Source")
    st.info(f"Directory: `{excel_directory}`")
    
    # Check if directory exists
    dir_path = Path(excel_directory)
    if dir_path.exists():
        excel_files = list(dir_path.glob("*.xlsx"))
        st.success(f"Found {len(excel_files)} Excel files")
        
        # Track processed files for new file detection
        if 'processed_files' not in st.session_state:
            st.session_state['processed_files'] = set()
        
        current_files = {file.name for file in excel_files}
        new_files = current_files - st.session_state['processed_files']
        
        if new_files:
            st.success(f"🆕 {len(new_files)} new file(s) detected: {', '.join(new_files)}")
        
        # Show file modification times to detect new files
        with st.expander("View Files & Status"):
            for file in excel_files:
                mod_time = datetime.fromtimestamp(file.stat().st_mtime)
                is_new = file.name in new_files
                if is_new:
                    st.markdown(f"🆕 **{file.name}**")
                else:
                    st.write(f"📄 {file.name}")
                st.caption(f"Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("Directory not found!")

with col2:
    st.subheader("🔄 Refresh Data")
    if st.button("Load/Refresh Data", type="primary"):
        with st.spinner("Processing Excel files..."):
            summary_df, files_df, combined_df, error = process_bom_data(excel_directory)
            
            if error:
                st.error(error)
            else:
                st.session_state['summary_data'] = summary_df
                st.session_state['files_data'] = files_df
                st.session_state['combined_data'] = combined_df
                st.session_state['raw_data'] = summary_df  # For filtering
                st.session_state['last_refresh'] = time.time()
                
                # Update processed files set
                dir_path = Path(excel_directory)
                if dir_path.exists():
                    current_files = {file.name for file in dir_path.glob("*.xlsx")}
                    st.session_state['processed_files'] = current_files
                
                st.success(f"✅ Loaded {len(summary_df)} unique items")

with col3:
    st.subheader("ℹ️ Last Refresh")
    if 'last_refresh' in st.session_state:
        refresh_time = st.session_state['last_refresh']
        st.info(f"Last refresh: {time.strftime('%H:%M:%S', time.localtime(refresh_time))}")
    else:
        st.info("No data loaded yet")

# Check if data is loaded
if 'summary_data' not in st.session_state:
    st.warning("👈 Click 'Load/Refresh Data' to start")
    st.stop()

summary_df = st.session_state['summary_data']
files_df = st.session_state['files_data']
combined_df = st.session_state['combined_data']

# Auto-refresh logic
if auto_refresh and 'last_refresh' in st.session_state:
    if time.time() - st.session_state['last_refresh'] > 30:
        with st.spinner("Auto-refreshing..."):
            summary_df, files_df, combined_df, error = process_bom_data(excel_directory)
            if not error:
                st.session_state['summary_data'] = summary_df
                st.session_state['files_data'] = files_df
                st.session_state['combined_data'] = combined_df
                st.session_state['raw_data'] = summary_df
                st.session_state['last_refresh'] = time.time()
                
                # Update processed files set
                dir_path = Path(excel_directory)
                if dir_path.exists():
                    current_files = {file.name for file in dir_path.glob("*.xlsx")}
                    st.session_state['processed_files'] = current_files
                
                st.rerun()

# Key Metrics
st.header("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Items", len(summary_df))

with col2:
    total_qty = summary_df['Units'].sum()
    st.metric("Total Quantity", f"{total_qty:,.0f}")

with col3:
    st.metric("Total Files", len(files_df['File'].unique()) if files_df is not None else 0)

with col4:
    st.metric("Total Tabs", len(files_df) if files_df is not None else 0)

# Quantity Total Table
st.header("📊 Quantity Total Table")

# Create tabs for different views of the quantity data
tab1, tab2, tab3 = st.tabs(["📋 Complete Summary", "📁 By Source File", "📈 Quantity Analysis"])

with tab1:
    st.subheader("Complete BOM Summary by Item")
    
    # Add some summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unique Items", len(summary_df))
    with col2:
        st.metric("Total Quantity", f"{summary_df['Units'].sum():,.0f}")
    with col3:
        st.metric("Avg Quantity per Item", f"{summary_df['Units'].mean():,.0f}")
    
    # Display the complete summary table
    st.dataframe(
        summary_df.style.format({
            'Units': '{:,.0f}'
        }).background_gradient(cmap='Blues', subset=['Units']),
        use_container_width=True,
        height=500
    )

with tab2:
    st.subheader("Quantity Breakdown by Source File")
    
    if files_df is not None and len(files_df) > 0:
        # Display file information with quantities
        file_summary = files_df.copy()
        file_summary['Modified'] = file_summary['Modified'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            file_summary.style.format({
                'Items': '{:,.0f}'
            }).background_gradient(cmap='Greens', subset=['Items']),
            use_container_width=True,
            height=300
        )
        
        # Create a bar chart showing items per file
        fig_files = px.bar(
            files_df,
            x='File',
            y='Items',
            title='Number of Items per Source File',
            color='Items',
            color_continuous_scale='Viridis'
        )
        fig_files.update_xaxes(tickangle=45)
        st.plotly_chart(fig_files, use_container_width=True)
    else:
        st.info("No file information available")

with tab3:
    st.subheader("Quantity Analysis")
    
    # Create quantity ranges
    summary_df_copy = summary_df.copy()
    summary_df_copy['Quantity Range'] = pd.cut(
        summary_df_copy['Units'],
        bins=[0, 100, 1000, 10000, float('inf')],
        labels=['1-100', '101-1,000', '1,001-10,000', '10,000+']
    )
    
    # Convert quantity range to string for display
    summary_df_copy['Quantity Range'] = summary_df_copy['Quantity Range'].astype(str)
    
    # Quantity range distribution
    range_counts = summary_df_copy['Quantity Range'].value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quantity Range Distribution")
        fig_range = px.bar(
            x=range_counts.index,
            y=range_counts.values,
            title='Items by Quantity Range',
            color=range_counts.values,
            color_continuous_scale='Plasma'
        )
        fig_range.update_xaxes(title='Quantity Range')
        fig_range.update_yaxes(title='Number of Items')
        st.plotly_chart(fig_range, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Items by Quantity")
        top_10 = summary_df.head(10)
        
        fig_top10 = px.bar(
            top_10,
            x='Units',
            y='Model/PN',
            orientation='h',
            title='Top 10 Items by Quantity',
            color='Units',
            color_continuous_scale='Inferno'
        )
        fig_top10.update_layout(height=400)
        st.plotly_chart(fig_top10, use_container_width=True)
    
    # Quantity statistics
    st.subheader("Quantity Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Min Quantity", f"{summary_df['Units'].min():,.0f}")
    with col2:
        st.metric("Max Quantity", f"{summary_df['Units'].max():,.0f}")
    with col3:
        st.metric("Median Quantity", f"{summary_df['Units'].median():,.0f}")
    with col4:
        st.metric("Std Dev", f"{summary_df['Units'].std():,.0f}")

# Project File Breakdown Table
st.header("📁 Project File Breakdown")

st.subheader("Units per Project File with Total")

if combined_df is not None and len(combined_df) > 0:
    # Create pivot table: Model/PN as rows, Source File as columns, Units as values
    pivot_df = combined_df.pivot_table(
        index='Model/PN',
        columns='Source File',
        values='Units',
        aggfunc='sum',
        fill_value=0
    )
    
    # Add total column
    pivot_df['Total'] = pivot_df.sum(axis=1)
    
    # Sort by total descending
    pivot_df = pivot_df.sort_values('Total', ascending=False)
    
    # Add Networking description back to the pivot table
    networking_map = combined_df.drop_duplicates('Model/PN').set_index('Model/PN')['Networking'].to_dict()
    pivot_df.insert(0, 'Networking', pivot_df.index.map(networking_map))
    
    # Display the pivot table
    st.dataframe(
        pivot_df.style.format({col: '{:,.0f}' for col in pivot_df.columns if col != 'Networking'})
        .background_gradient(cmap='YlOrRd', subset=[col for col in pivot_df.columns if col != 'Networking'])
        .set_properties(**{'text-align': 'right'}),
        use_container_width=True,
        height=600
    )
    
    # Show summary statistics for the pivot table
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items in Matrix", len(pivot_df))
    with col2:
        st.metric("Total Project Files", len([col for col in pivot_df.columns if col != 'Networking' and col != 'Total']))
    with col3:
        st.metric("Grand Total", f"{pivot_df['Total'].sum():,.0f}")
    
    # Export option for the pivot table
    if st.button("Export Project File Breakdown to Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pivot_df.to_excel(writer, sheet_name='Project Breakdown')
        
        st.download_button(
            label="Download Project Breakdown Excel",
            data=output.getvalue(),
            file_name=f"Project_File_Breakdown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No combined data available for project file breakdown")

# Query Section
st.header("🔍 Query Data")

with st.expander("Click to expand query options"):
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search by Model/PN or Networking description")
        min_qty = st.number_input("Minimum Quantity", min_value=0, value=0)
    
    with col2:
        max_qty = st.number_input("Maximum Quantity", min_value=0, value=None)
        top_n = st.number_input("Show Top N Items", min_value=1, value=20)
    
    # Apply filters
    filtered_df = summary_df.copy()
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Model/PN'].str.contains(search_term, case=False, na=False) |
            filtered_df['Networking'].str.contains(search_term, case=False, na=False)
        ]
    
    if min_qty > 0:
        filtered_df = filtered_df[filtered_df['Units'] >= min_qty]
    
    if max_qty is not None and max_qty > 0:
        filtered_df = filtered_df[filtered_df['Units'] <= max_qty]
    
    # Store filtered data for export
    st.session_state['filtered_data'] = filtered_df
    
    st.info(f"Showing {len(filtered_df)} of {len(summary_df)} items")
    
    # Display filtered data
    if len(filtered_df) > 0:
        st.subheader("Query Results")
        display_df = filtered_df.head(top_n)
        st.dataframe(
            display_df.style.format({
                'Units': '{:,.0f}'
            }),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("No results match your query. Try adjusting the criteria.")

# Data Visualization
st.header("📊 Data Visualization")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Items by Quantity")
    top_items = summary_df.head(15)
    
    # Create a label that combines Networking description with quantity
    top_items['Label'] = top_items['Networking'].apply(lambda x: str(x)[:30] + '...' if len(str(x)) > 30 else str(x))
    
    fig_bar = px.bar(
        top_items,
        x='Model/PN',
        y='Units',
        title='Top 15 Items by Quantity',
        color='Units',
        color_continuous_scale='Blues',
        text='Label',
        hover_data=['Networking', 'Units']
    )
    fig_bar.update_xaxes(tickangle=45)
    fig_bar.update_traces(textposition='outside', textfont_size=10)
    fig_bar.update_layout(height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Quantity Distribution")
    pie_data = summary_df.head(10).copy()
    # Create custom labels with Networking descriptions
    pie_data['Custom Names'] = pie_data['Model/PN'] + '\n(' + pie_data['Networking'].apply(lambda x: str(x)[:20] + '...' if len(str(x)) > 20 else str(x)) + ')'
    
    fig_pie = px.pie(
        pie_data,
        values='Units',
        names='Custom Names',
        title='Quantity Distribution (Top 10 Items)',
        hole=0.4,
        hover_data=['Networking', 'Units']
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Detailed Table
st.header("📋 Complete BOM Summary")

with st.expander("View Complete Summary Table"):
    st.dataframe(
        summary_df.style.format({
            'Units': '{:,.0f}'
        }),
        use_container_width=True,
        height=600
    )

# File Information
st.header("📄 Source File Information")

if files_df is not None and len(files_df) > 0:
    st.dataframe(
        files_df,
        use_container_width=True,
        height=300
    )

# Export functionality
st.header("📤 Export Data")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Export Complete Summary to Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name='BOM Summary', index=False)
            if files_df is not None:
                files_df.to_excel(writer, sheet_name='File Info', index=False)
        
        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name=f"L11_Networking_Forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col2:
    if st.button("Export Complete Summary to CSV"):
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download CSV File",
            data=csv,
            file_name=f"L11_Networking_Forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("Export Query Results to CSV"):
        if 'filtered_data' in st.session_state and len(st.session_state['filtered_data']) > 0:
            csv = st.session_state['filtered_data'].to_csv(index=False)
            st.download_button(
                label="Download Query Results CSV",
                data=csv,
                file_name=f"L11_Networking_Query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No query results available. Please run a query first.")

# Quarterly Forecast Section (placeholder for future enhancement)
st.header("📅 Quarterly Forecast Analysis")
st.info("""
**Quarterly Forecast Feature**: This section can be enhanced to provide quarterly forecasting analysis.
Currently, the dashboard shows total quantities. To enable quarterly forecasting, the source Excel files
would need to include quarterly breakdown data or delivery schedules.

**Future Enhancements**:
- Add quarterly delivery schedule parsing
- Implement forecast trend analysis
- Add quarter-over-quarter comparison
- Include demand planning metrics
""")

# Deployment Instructions
st.header("🚀 Deployment & Sharing Instructions")
with st.expander("How to share this dashboard internally within Dell"):
    st.markdown("""
    ### Option 1: Streamlit Cloud (Recommended for sharing)
    1. Push this code to a GitHub repository
    2. Connect the repository to Streamlit Cloud (share.streamlit.io)
    3. Deploy the app and share the URL with your team
    4. Ensure the Excel files are accessible (either in the repo or via cloud storage)

    ### Option 2: Internal Server Deployment
    1. Install Streamlit on a Dell internal server: `pip install streamlit`
    2. Run the dashboard: `streamlit run l11_networking_forecast.py`
    3. Make the server accessible internally via VPN or intranet
    4. Share the server URL with your team

    ### Option 3: Share Code for Local Execution
    1. Share the Python script and requirements.txt
    2. Team members can run locally: `streamlit run l11_networking_forecast.py`
    3. Each user needs access to the Excel files directory

    ### Requirements
    - Python 3.8+
    - streamlit
    - pandas
    - plotly
    - openpyxl
    """)

# Footer
st.markdown("---")
st.markdown("""
**L11 Networking Forecast Agent** | Built with Streamlit | 
<span class="dell-blue">Dell Internal Use</span>
""", unsafe_allow_html=True)
