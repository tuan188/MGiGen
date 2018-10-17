final class {{ class_name }}Mock: {{ protocol_name }} {
{% for f in functions %}
    // MARK: - {{ f.name }}
    
    var {{ f.name }}_Called = false
{% if not f.return_void %}
    var {{ f.name }}_ReturnValue: {{ f.return_type }} = {{ f.return_value }}
{% endif %}

    {{ f.origin }} {
        {{ f.name }}_Called = true
    {% if not f.return_void %}
        return {{ f.name }}_ReturnValue
    {% endif %}
    }
    
{% endfor %}
}