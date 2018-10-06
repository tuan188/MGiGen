extension {{ name }} {
    init() {
        self.init(
        {% for p in properties %}
            {{ p.name }}: {{ p.value }}{{ "," if not loop.last }}
        {% endfor %}
        )
    }
}