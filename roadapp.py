import os
import math
from PIL import Image

import streamlit as st
import pandas as pd

# import custom formula library
from modules.util import formulas

# ----------------------/---------------------- #
# Reading data from excel - this is so that people can edit the excel rather than edit the code
formula_sheet_path = r"spreadsheets/formulas.xlsx"
data_sheet_path = os.path.join(os.path.dirname(__file__), formula_sheet_path)

emoji = '🔥📐✏️✍️🧠📖💡🏎️🧐👓👀'

# Get formula from excel
df = pd.read_excel(data_sheet_path, sheet_name="formulas")

# Adverse Crossfall
f1 = df.iloc[0, 1]
f2 = df.iloc[1, 1]
f3 = df.iloc[1, 2]


# ----------------------/ APP LAYOUT /---------------------- #
# App Title
st.title("Aurecon Road Design Tool")

# Add a breakline
# st.write("---")

# Add some space
# st.markdown('<br><br>', unsafe_allow_html=True)





# Setup Tables
# Create look up table
# Austroads Part 3, Section 3.3
speed_data = pd.DataFrame({
	'Design': [50, 60, 70, 80, 90, 100, 110, 120],
	'Posted': [40, 50, 60, 70, 80, 90, 100, 110]
})

# Austroads Part 3, Section 8.6.8
max_grade_change = pd.DataFrame({
	'Speed': [40, 50, 60, 70, 80, 90, 100, 110, 120],
	'Grade Change': [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
})



def adverse_crossfall():
	with st.container(border=True):
		st.write("📖 Formula")

		# display_formula = st.latex(r'''R = V^2 / (127(e+f))''')
		# st.latex(r'R = \frac {V^2} {127 * (e + f) }') # This is a nicer format on fraction
		display_fm_R = formulas.adverse_crossfall_fm_R()[0]
		st.latex(display_fm_R)
		# st.latex(str(f1)) # Get formula from excel

	with st.container(border=True):
		st.write("✍️ Inputs")

		col1, col2 = st.columns(2)
		# Variable Inputs
		V = col1.number_input(label="V - Design Speed", value=100.00)
		f = col1.number_input(label="f - Side Friction", value=0.11)
		e = col2.number_input(label="e - Super", value=-0.03)

		# Calculation
		R = eval(formulas.adverse_crossfall_fm_R()[1])

	with st.container(border=True):
		st.write("📐 Results")
		# Display Results
		st.markdown("<h1 style='font-size: 24px; text-align: left;'>R - Minimum Radius:</h1>", unsafe_allow_html=True)
		st.markdown(f"<h1 style='font-size: 36px; text-align: center; border: 1px solid;'>{R} m</h1>", unsafe_allow_html=True)
		st.markdown("<br>", unsafe_allow_html=True)

	with st.expander(label='REFERENCE TABLE', expanded=True, icon="🧐"):
		# Setup a image
		image_path = r'./modules/adverse_crossfall/docs/media/table_7.12.png'
		image = Image.open(image_path)
		st.image(image)


def vert_geo():
	with st.expander(label=f"Speed", expanded=True, icon='🏎️'):
		# Setup layout
		col1, col2, col3 = st.columns([1, 1, 0.5])

		# Create a selectbox for Design Speeds
		design_speed = col1.selectbox("Design Speed:", speed_data['Design'])

		# Create a override field and a reset button
		if "override" not in st.session_state:
			st.session_state.override = 0

		def reset_number_input():
			st.session_state.override = 0

		override = col2.number_input("Override:", key="override")

		col3.markdown("<br>", unsafe_allow_html=True)
		button = col3.button("Clear Override", on_click=reset_number_input)
		
		if override:
			result = override
		else:
			result = speed_data[speed_data["Design"] == design_speed]["Posted"].values[0]
			
		st.write(f"Posted Speed: {result} km/h")

	with st.container(border=True):
		sub_title_1 = r'Max grade change without a vertical curve'
		sub_title_2 = r'Refer to Austroads Part3, Section 8.6.8 Table 8.10'
		st.markdown(f"<h1 style='font-size: 16px; text-align: left;'>{sub_title_1}:</h1>", unsafe_allow_html=True)
		st.markdown(f"<h3 style='font-size: 14px; text-align: left;'>{sub_title_2}:</h3>", unsafe_allow_html=True)
		st.markdown("<br>", unsafe_allow_html=True)

		# Display Formula
		with st.container(border=True):
			st.write("📖 Formula")
			f = r"Grade Change = | |Grade OUT|  - |Grade IN| |"
			st.latex(f)

		with st.container(border=True):
			st.write("✍️ Inputs")
			col1, col2 = st.columns(2)
			grade_out = col1.number_input("Grade OUT (%):", value=-6.9)
			grade_in = col2.number_input("Grade IN (%):", value=7.9)

			# Calculation
			grade_change = abs(abs(grade_in / 100) - abs(grade_out / 100))

		with st.container(border=True):
			st.write("📐 Results")
			st.markdown("<h2 style='font-size: 16px; text-align: left;'>Grade Change:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{grade_change* 100:.2f} %</h2>", unsafe_allow_html=True)

			max_allowed = max_grade_change[max_grade_change["Speed"] == design_speed]["Grade Change"].values[0]
			st.markdown("<h2 style='font-size: 16px; text-align: left;'>Max Allowed:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{max_allowed:.2f} %</h2>", unsafe_allow_html=True)
			st.markdown("<br>", unsafe_allow_html=True)

	with st.expander(label=f"REFERENCE TABLE", expanded=True, icon="🧐" ):
		col1, col2 = st.columns(2)

		col1.write(r'Austroads Part 3, Section 3.3')
		col1.dataframe(speed_data, use_container_width=True, hide_index=True)

		col2.write(r'Austroads Part 3, Section 8.6.8')
		col2.dataframe(max_grade_change, use_container_width=True, hide_index=True)
		

def crest_curves():
	# Display Formula
	with st.container(border=True):
		st.write("📖 Formula")
		display_fm_S = formulas.crest_curves_fm_S()[0]
		display_fm_K = formulas.crest_curves_fm_K()[0]
		st.latex(display_fm_S)
		st.latex(display_fm_K)

	col1, col2 = st.columns(2)
	with col1.container(border=True):
		st.write("🚗 Cars")

		# Variable Inputs
		V = st.number_input(label="V - Design Speed", value=100.00, key="V_01")
		RT = st.number_input(label="RT", value=3.0, key="RT_01")
		d = st.number_input(label="d", value=0.15, key="d_01")
		a = st.number_input(label="a", value=0, key="a_01")
		
		# Calculation formula
		S = eval(formulas.crest_curves_fm_S()[1])

		# Display result
		st.markdown("<h2 style='font-size: 16px; text-align: left;'>S - Sight Distance:</h2>", unsafe_allow_html=True)
		st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{S:.2f} m</h2>", unsafe_allow_html=True)
		
		# Variable Inputs
		h_1 = st.number_input(label="H1 - Eye Height", value=1.1, key="h_1_01")
		h_2 = st.number_input(label="H2 - Object Height", value=0.2, key="h_2_01")

		# Calculation formula
		K = eval(formulas.crest_curves_fm_K()[1])

		# Display result
		st.markdown("<h2 style='font-size: 16px; text-align: left;'>K:</h2>", unsafe_allow_html=True)
		st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{K:.2f}</h2>", unsafe_allow_html=True)

		st.write("---")
		st.markdown("<h1 style='font-size: 24px; text-align: left;'>Minimum Radius - Cars:</h1>", unsafe_allow_html=True)
		st.markdown(f"<h1 style='font-size: 36px; text-align: center; border: 1px solid;'>{K*100:.2f} m</h1>", unsafe_allow_html=True)
		st.markdown("<br>", unsafe_allow_html=True)
		

	with col2.container(border=True):
		st.write("🚚 Trucks")
		# Variable Inputs
		V = st.number_input(label="V - Design Speed", value=80.00, key="V_02")
		RT = st.number_input(label="RT", value=2.0, key="RT_02")
		d = st.number_input(label="d", value=0.20, key="d_02")
		a = st.number_input(label="a", value=0, key="a_02")
		
		# Calculation formula
		S = eval(formulas.crest_curves_fm_S()[1])

		# Display result
		st.markdown("<h2 style='font-size: 16px; text-align: left;'>S - Sight Distance:</h2>", unsafe_allow_html=True)
		st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{S:.2f} m</h2>", unsafe_allow_html=True)

		# Variable Inputs
		h_1 = st.number_input(label="H1 - Eye Height", value=2.4, key="h_1_02")
		h_2 = st.number_input(label="H2 - Object Height", value=0.2, key="h_2_02")

		# Calculation formula
		K = eval(formulas.crest_curves_fm_K()[1])

		# Display result
		st.markdown("<h2 style='font-size: 16px; text-align: left;'>K:</h2>", unsafe_allow_html=True)
		st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{K:.2f}</h2>", unsafe_allow_html=True)

		st.write("---")
		st.markdown("<h1 style='font-size: 24px; text-align: left;'>Minimum Radius - Trucks:</h1>", unsafe_allow_html=True)
		st.markdown(f"<h1 style='font-size: 36px; text-align: center; border: 1px solid;'>{K*100:.2f} m</h1>", unsafe_allow_html=True)
		st.markdown("<br>", unsafe_allow_html=True)


	with st.expander(label='REFERENCE TABLE', expanded=True, icon="🧐"):
		# Setup a image
		image_path = r'./modules/crest_curves/docs/media/table_8.7.png'
		image = Image.open(image_path)
		st.image(image)


def aquaplaning():
	# Display Formula
	display_fm_D = formulas.aquaplaning_fm_D()[0]
	display_fm_L = formulas.aquaplaning_fm_L()[0]
	display_fm_S = formulas.aquaplaning_fm_S()[0]

	with st.expander(label="Where no super transition", expanded=True):
		with st.container(border=True):
			st.write("📖 Formula")
			st.latex(display_fm_S)
			st.latex(display_fm_L)		

		with st.container(border=True):
			st.write("✍️ Inputs")
			col1, col2 = st.columns([1,1])
			D = col1.number_input(label=r"D - Water Film Depth (mm)", value=2.5, key="D1")
			T = col1.number_input(label=r"T - Average Pavement Texture Depth (mm)", value=0.4, key="T1")
			I = col1.number_input(label=r"I - Rainfall Intensity (mm/hr)", value=50.0, key="I1")
			pave_cross_fall = col2.number_input(label=r"Pavement Crossfall (%)", value=3.0, key="cf1")
			long_grade = col2.number_input(label=r"Longitudinal Grade (%)", value=0.5, key="lg1")

			# Calculation

			S = eval(formulas.aquaplaning_fm_S()[1])
			L = eval(formulas.aquaplaning_fm_L()[1])

		with st.container(border=True):
			st.write("📐 Results")
			st.markdown("<h2 style='font-size: 16px; text-align: left;'>S - Slop of Drainage Path:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{S:.3f} %</h2>", unsafe_allow_html=True)

			st.markdown("<h2 style='font-size: 16px; text-align: left;'>L - Length of Drainage Path:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{L:.3f} m</h2>", unsafe_allow_html=True)
			st.markdown(r"<br>", unsafe_allow_html=True)

	st.write("---")

	with st.expander(label="Where there is superelevation", expanded=True):
		with st.container(border=True):
			st.write("📖 Formula")
			st.latex(display_fm_L)			

		with st.container(border=True):
			st.write("✍️ Inputs")
			col1, col2 = st.columns([1,1])
			D = col1.number_input(label=r"D - Water Film Depth (mm)", value=3.0, key="D2")
			T = col1.number_input(label=r"T - Average Pavement Texture Depth (mm)", value=0.4, key="T2")
			I = col2.number_input(label=r"I - Rainfall Intensity (mm/hr)", value=50.0, key="I2")
			S = col2.number_input(label=r"S - Slope of Drainage Path (%)", value=0.96, key="S2")

			# Calculation
			L = eval(formulas.aquaplaning_fm_L()[1])

		with st.container(border=True):
			st.write("📐 Results")
			st.markdown("<h2 style='font-size: 16px; text-align: left;'>L - Length of Drainage Path:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{L:.3f} m</h2>", unsafe_allow_html=True)
			st.markdown(r"<br>", unsafe_allow_html=True)

	st.write("---")

	with st.expander(label="Where there is superelevation", expanded=True):
		with st.container(border=True):
			st.write("📖 Formula")
			st.latex(display_fm_S)
			st.latex(display_fm_D)	

		with st.container(border=True):
			st.write("✍️ Inputs")
			col1, col2 = st.columns([1,1])
			T = col1.number_input(label=r"T - Average Pavement Texture Depth (mm)", value=0.4, key="T3")
			I = col1.number_input(label=r"I - Rainfall Intensity (mm/hr)", value=50.0, key="I3")
			H = col2.number_input(label=r"Height Difference (m)", value=0.23, key="H3")
			L = col2.number_input(label=r"Measured Drainage Path Length (m)", value=17.3, key="L3")

			# Calculation
			S = H / L
			D = eval(formulas.aquaplaning_fm_D()[1])

		with st.container(border=True):
			st.write("📐 Results")
			st.markdown("<h2 style='font-size: 16px; text-align: left;'>S - Slop of Drainage Path:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{S:.3f} %</h2>", unsafe_allow_html=True)

			st.markdown("<h2 style='font-size: 16px; text-align: left;'>D - Water Film Depth:</h2>", unsafe_allow_html=True)
			st.markdown(f"<h2 style='font-size: 24px; text-align: center; border: 1px solid;'>{D:.2f} mm</h2>", unsafe_allow_html=True)
			st.markdown(r"<br>", unsafe_allow_html=True)


parent_tab_1, parent_tab_2, parent_tab_3 = st.tabs([r"QLD", r"NSW", r"SAVI"])

with parent_tab_1:

	# Setup Tabs
	tab_name_01 = r"1 . Horizontal Geometry"
	tab_name_02 = r"2 . Horizontal Curves & Super"
	tab_name_03 = r"3 . Adverse Crossfall"
	tab_name_04 = r"4 . Vertical Geometry"
	tab_name_05 = r"5 . Crest Curves - Sealed Roads"
	tab_name_08 = r"8 . Aquaplaning"
	tab_name_00 = r"test"

	test_tab, tab_1, tab_2, tab_3, tab_4, tab_5, tab_8 = st.tabs([
		tab_name_00, 
		tab_name_01,
		tab_name_02,
		tab_name_03, 
		tab_name_04, 
		tab_name_05, 
		tab_name_08
		])

	with tab_3:
		adverse_crossfall()

	with tab_5:
		crest_curves()

	with tab_4:
		vert_geo()

	with tab_8:
		aquaplaning()

with parent_tab_2:
	st.write("TBC")

with parent_tab_3:
	st.write("TBC")


import streamlit.components.v1 as v1

with test_tab:
	tab0, tab1 = st.tabs(["🧐 sub_tab_1", "sub_tab_2"])
	with tab0:
		# data_table_path = r"C:\Users\David.Ge\repo\Aurecon Github\Aurecon-road-app\spreadsheets\tables.xlsx"
		# xls = pd.ExcelFile(data_table_path)
		# dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

		# # Selection box
		# selected_sheet = st.selectbox("Select a sheet", list(dfs.keys()))

		# # List of selections
		# # st.write(list(dfs.keys()))

		# # Selected data
		# # st.write(r"Selected Data")
		# # st.write(dfs[selected_sheet])

		# data_name = dfs[selected_sheet].columns[0]
		# table_name = dfs[selected_sheet].iloc[0,0]

		# new_col_names = dfs[selected_sheet].iloc[1]
		# # st.write(r"Column Headings")
		# # st.write(new_col_names)

		# # Remove the first 2 rows by splitting
		# dfs[selected_sheet] = dfs[selected_sheet].iloc[2:]
		# # st.write(r"Cleaned Data")
		# # st.write(dfs[selected_sheet])
		
		# dfs[selected_sheet].columns = new_col_names
		# st.write(data_name)
		# st.write(table_name)
		# st.write(dfs[selected_sheet])

		# Create two input fields for width and height
		width = st.slider("Enter width:", value=500, min_value=1)
		height = st.slider("Enter height:", value=100, min_value=1)

		# Define the HTML and CSS for the dynamic box shape
		# html_string = f'''
		# <div class="box-shape" style="width: {width}px; height: {height}px;"></div>
		# <style>
		# 	.box-shape {{
		# 		background-color: #3498db;
		# 		border: 1px solid #2980b9;
		# 	}}
		# </style>
		# '''

		html_string = f'''
		<div class="triangle-shape" style="width: 0; height: 0; border-left: {width}px solid transparent; border-right: {width}px solid transparent; border-bottom: {height}px solid #3498db;"></div>
		<style>
			.triangle-shape {{
				display: inline-block;
				margin-top: 10px;
			}}
		</style>
		'''

		# Display the dynamic box shape
		v1.html(html_string)


# Testing locating reference tables in the side bar
with st.sidebar:
	# side_tab1 = st.tabs(["Reference Table"])
	formula_sheet_path = r"spreadsheets/tables.xlsx"
	data_sheet_path = os.path.join(os.path.dirname(__file__), formula_sheet_path)
	# df = pd.read_excel(file_path, 3)

	# # Get the column names from the table
	# column_names = df.columns

	# # Set the side bar title 
	# st.sidebar.header(column_names[0])
	st.sidebar.header("Reference Tables")
	
	# # Use the first data row as the column headers
	# headers = df.iloc[0].values
	# df.columns = headers

	# # st.sidebar.header(df.iloc[0,0])
	
	# # Remove the first data row
	# df = pd.DataFrame(df[1:])
	# st.dataframe(df, use_container_width=True, hide_index=True)



	xls = pd.ExcelFile(data_sheet_path)
	dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

	selected_sheet = st.selectbox("Select a table", list(dfs.keys()))
	df = pd.read_excel(data_sheet_path, selected_sheet)

	# Get the column names from the table
	column_names = df.columns

	# Set the side bar title 
	st.sidebar.header(column_names[0])
	# st.sidebar.header("Reference Tables")
	
	# Use the first data row as the column headers
	headers = df.iloc[0].values
	df.columns = headers

	# st.sidebar.header(df.iloc[0,0])
	
	# Remove the first data row
	df = pd.DataFrame(df[1:])
	st.dataframe(df, use_container_width=True, hide_index=True)