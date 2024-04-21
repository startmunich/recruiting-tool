mkdir -p ~/.streamlit/
echo "
[server]\n
headless = true\n
port = $PORT\n
enableCORS = false\n
" > ~/.streamlit/config.toml

mkdir .data
touch .data/applications.json
touch .data/evaluations.json
touch .data/users.json