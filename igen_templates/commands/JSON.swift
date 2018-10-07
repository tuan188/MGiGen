struct {{ name }} {
{% for p in properties %}
    var {{ p.name }}: {{ p.type_name }}
{% endfor %}
}

extension {{ name }} {
    init() {
        self.init(
        {% for p in properties %}
            {{ p.name }}: {{ p.value }}{{ "," if not loop.last }}
        {% endfor %}
        )
    }
}

extension {{ name }}: Then { }

extension {{ name }}: Mappable {
    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
{% for p in properties %}
    {% if p.is_date %}
        {{ p.name }} <- (map["{{ p.raw_name }}"], DateTransform())
    {% else %}
        {{ p.name }} <- map["{{ p.raw_name }}"]
    {% endif %}
{% endfor %}
    }
}
