{% if is_protocol %}
final class {{ class_name }}Mock: {{ protocol_name }} {

{% endif %}
    {% for f in functions %}
    // MARK: - {{ f.overloaded_name }}

    var {{ f.overloaded_name }}Called = false
    {% if not f.return_void %}
    {% if f.return_nil %}
    var {{ f.overloaded_name }}ReturnValue: {{ f.return_type }} = {{ f.return_value }}
    {% else %}
    var {{ f.overloaded_name }}ReturnValue = {{ f.return_value }}
    {% endif %}
    {% endif %}

    {{ f.origin }} {
        {{ f.overloaded_name }}Called = true
    {% if not f.return_void %}
        return {{ f.overloaded_name }}ReturnValue
    {% endif %}
    } {{ '\n' if not loop.last }}
    {% endfor %}
{{ '}' if is_protocol }}