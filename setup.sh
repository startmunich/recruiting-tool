mkdir -p ~/.streamlit/
echo "
[theme]\n
primaryColor=\"#CA1551\"\n
backgroundColor=\"#FFFFFF\"\n
textColor=\"#011152\"\n
font=\"sans serif\"\n
[client]\n
toolbarMode = \"minimal\"\n
showSidebarNavigation = false\n
[server]\n
headless = true\n
port = $PORT\n
enableCORS = false\n
" > ~/.streamlit/config.toml

mkdir .data
touch .data/applications.json
touch .data/evaluations.json
touch .data/users.json