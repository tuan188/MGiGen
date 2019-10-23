final class {{ name }}: Mappable {
    {% for p in properties %}
    {% if p.is_optional %}
    var {{ p.name }}: {{ p.type_name }}
    {% elif p.is_swift_type %}
    var {{ p.name }} = {{ p.value }}
    {% else %}
    var {{ p.name }}: {{ p.type_name }} = {{ p.value }}
    {% endif %}
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

    init() {

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
