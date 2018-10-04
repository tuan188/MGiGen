struct {{ model_name }}ViewModel {
    let {{ model_variable }}: {{ model_name }}
    
    {% for p in properties %}
    var {{ p.name }}: String {
        return ""
    }
        
    {% endfor %}
}
