extension {{ name }} {
    init() {
        self.init(
        {% for p in properties %}
            {{ p.name }}: {{ p.type.default_value }}{{ "," if not loop.last }}
        {% endfor %}
        )
    }
}