# Formula Library


# Aquaplaning
def aquaplaning_fm_D():
	Aquaplaning_fm_D_latex = r"D = \frac{0.103 * T^{0.11} * L^{0.43} * I^{0.59}} {S^{0.42}} - T"
	Aquaplaning_fm_D_string = r"( (0.103 * T**0.11 * L**0.43 * I**0.59) / (S*100)**0.42 ) - T"
	return Aquaplaning_fm_D_latex, Aquaplaning_fm_D_string

def aquaplaning_fm_L():
	Aquaplaning_fm_L_latex = r"L = [ \frac{(D + T)*S^{0.42}}  {(0.103*T^{0.11})*I^{0.59}}] ^ {\frac{1}{0.43}}"
	Aquaplaning_fm_L_string = r"((D + T) * S**0.42 / (0.103 * T**0.11 * I**0.59))**(1/0.43)"
	return Aquaplaning_fm_L_latex, Aquaplaning_fm_L_string

def aquaplaning_fm_S():
	Aquaplaning_fm_S_latex = r"S = (Pavement Crossfall ^ 2 + Longitudinal Grade ^ 2) ^ {0.5}"
	Aquaplaning_fm_S_string = r"(pave_cross_fall**2 + long_grade**2)**0.5"
	return Aquaplaning_fm_S_latex, Aquaplaning_fm_S_string


# Crest Curves
def crest_curves_fm_S():
	crest_curves_fm_S_latex = r"S = RT * \frac{V}{3.6} + \frac {V^2}  {254 * (d + 0.01 * a)}"
	crest_curves_fm_S_string = r"RT * V / 3.6 + V**2 / (254 * (d + 0.01 * a))"
	return crest_curves_fm_S_latex, crest_curves_fm_S_string

def crest_curves_fm_K():
	crest_curves_fm_K_latex = r"K = \frac{S^2}{200 * ( \sqrt{h_1} + \sqrt{h_2} )^2}"
	crest_curves_fm_K_string = r"S**2 / (200 * (math.sqrt(h_1) + math.sqrt(h_2) )**2)"
	return crest_curves_fm_K_latex, crest_curves_fm_K_string


# Adverse Crossfall
def adverse_crossfall_fm_R():
	adverse_crossfall_fm_R_latex = r"R = \frac {V^2} {127 * (e + f) }"
	adverse_crossfall_fm_R_string = r"V**2 / (127 * (e + f))"
	return adverse_crossfall_fm_R_latex, adverse_crossfall_fm_R_string


# Formula shown in the "Shark Tank" event
def Pw():
	Pw_latex = r"P_w = \frac{wRT_1}{28.97ne}  \Bigl[\Bigl(\frac{P_1}{P_1}\Bigl)^{0.283} - 1 \Bigl]"
	return Pw_latex
