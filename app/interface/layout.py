import os
import streamlit as st


@st.dialog("ℹ️ How to Use the App")
def show_help_modal():
    """Renders a central pop-up with instructions and valid ticker examples."""
    st.markdown("""
    ### Instructions:
    - Enter the stock ticker symbol in the input field.
    - Click the **Analyze** button below to get real-time analysis, visualizations, and AI-generated insights.
    
    ### Examples of valid tickers:
    - **MSFT** (Microsoft)
    - **TSLA** (Tesla)
    - **PETR4.SA** (Petrobras - B3)
    - **GOOG** (Alphabet)
    
    *More tickers can be found here: [Nasdaq Stocks List](https://stockanalysis.com/list/nasdaq-stocks/)**
    """)

@st.dialog("⚠️ Purpose & Legal Disclaimer")
def show_disclaimer_modal():
    """Renders a central pop-up with the app's purpose and a strong legal disclaimer."""
    st.markdown("""
    ### App Purpose
    This application performs advanced real-time analysis of stock prices using AI Agents to support analytical strategies and data visualization.
    
    ### 🛑 Disclaimer
    **Use at your own risk.** This application is for educational and informational purposes only. The AI-generated insights, charts, and data **do not constitute financial advice**, recommendations, or inducements to trade. 
    
    The creator is not responsible for any financial losses, damages, or decisions made based on the use of this tool. Always conduct your own research or consult a certified financial advisor before making investment decisions.
    """)


class AppLayout:
    """Class responsible for rendering the main layout and styling the UI."""

    def __init__(
        self, 
        github_url: str = "https://github.com/viniciusrubens", 
        linkedin_url: str = "https://linkedin.com/in/viniciusrubens"
    ):
        """Initializes the layout with social links."""
        self.github_url = github_url
        self.linkedin_url = linkedin_url

    def apply_custom_style(self):
        """Reads custom CSS from the style.css file and injects it to override Streamlit styles."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "style.css")
        
        try:
            with open(css_file_path, "r") as css_file:
                custom_css = css_file.read()
                st.markdown(f"<style>\n{custom_css}\n</style>", unsafe_allow_html = True)
        except FileNotFoundError:
            st.error(f"Error: CSS file not found at {css_file_path}")

    def render_top_bar(self):
        """
        Renders the top navigation bar with pretty, distinct social icons 
        and a properly spaced Legal button.
        """
        empty_l, gh_col, li_col, legal_col = st.columns([8, 1.2, 1.2, 1.6])
        
        github_icon_url = "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/brands/github.svg"

        linkedin_icon_url = "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/brands/linkedin.svg"

        with gh_col:
            st.markdown(f'<a href="{self.github_url}" target="_blank" class="social-icon-link"><img src="{github_icon_url}" class="github-icon" alt="GitHub"></a>', unsafe_allow_html = True)
            
        with li_col:
            st.markdown(f'<a href="{self.linkedin_url}" target="_blank" class="social-icon-link"><img src="{linkedin_icon_url}" class="linkedin-icon" alt="LinkedIn"></a>', unsafe_allow_html = True)
            
        with legal_col:
            if st.button("⚖️ Legal", help = "Read Purpose and Disclaimer"):
                show_disclaimer_modal()

    def render_header(self) -> str:
        """
        Renders the main title, relocated help button, and search input.
        Must be called within a centered column in main.py.
        
        Returns:
            str: The ticker symbol entered by the user.
        """
        col_title, col_help = st.columns([11, 1])
        with col_title:
            st.header("Trading Analytics")
        with col_help:
            st.write("")
            if st.button("Help", help = "Click to see how to use"):
                show_help_modal()
        
        ticker = st.text_input("Enter the Ticker Symbol (e.g., AAPL):", placeholder = "e.g. MSFT", label_visibility = "collapsed").upper()
        
        return ticker