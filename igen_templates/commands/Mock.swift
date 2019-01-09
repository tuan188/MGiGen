{% if is_protocol %}
final class {{ class_name }}Mock: {{ protocol_name }} {
    
{% endif %}
{% for f in functions %}
    // MARK: - {{ f.name }}
    
    var {{ f.name }}Called = false
{% if not f.return_void %}
    var {{ f.name }}ReturnValue: {{ f.return_type }} = {{ f.return_value }}
{% endif %}

    {{ f.origin }} {
        {{ f.name }}Called = true
    {% if not f.return_void %}
        return {{ f.name }}ReturnValue
    {% endif %}
    } {{ '\n' if not loop.last }}
{% endfor %}
{{ '}' if is_protocol }}