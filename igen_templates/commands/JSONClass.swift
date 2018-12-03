final class {{ name }}: Mappable {
{% for p in properties %}
    var {{ p.name }}: {{ p.type_name }}
{% endfor %}

    init(
    {% for p in properties %}
        {{ p.name }}: {{ p.type_name }}{{ "," if not loop.last }}
    {% endfor %}
        ) {
    {% for p in properties %}
        self.{{ p.name }} = {{ p.name }}
    {% endfor %}
    }
    
    convenience init() {
        self.init(
        {% for p in properties %}
            {{ p.name }}: {{ p.value }}{{ "," if not loop.last }}
        {% endfor %}
        )
    }
    
    required convenience init?(map: Map) {
        self.init()
    }
    
    func mapping(map: Map) {
{% for p in properties %}
    {% if p.is_date %}
        {{ p.name }} <- (map["{{ p.raw_name }}"], DateTransform())
    {% else %}
        {{ p.name }} <- map["{{ p.raw_name }}"]
    {% endif %}
{% endfor %}
    }
}

extension {{ name }}: Then { }
