mkdir -p ~/.streamlit/
echo "
[theme]\n
primaryColor=\"#CA1551\"\n
backgroundColor=\"#00002C\"\n
secondaryBackgroundColor=\"#011152\"\n
textColor=\"#FFFFFF\"\n
font=\"sans serif\"\n
[client]\n
toolbarMode = \"viewer\"\n
showSidebarNavigation = false\n
[server]\n
headless = true\n
port = $PORT\n
enableCORS = false\n
" > ~/.streamlit/config.toml