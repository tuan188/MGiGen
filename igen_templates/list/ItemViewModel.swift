struct {{ model_name }}ItemViewModel {
    {% for p in properties %}
    let {{ p.name }}: String      
    {% endfor %}

    init({{ model_variable }}: {{ model_name }}) {
        {% for p in properties %}
        self.{{ p.name }} = ""    
        {% endfor %}
    }
}
