import UIKit
import Reusable

final class {{ model_name }}Cell: UITableViewCell, NibReusable {
{% for p in properties %}
    @IBOutlet weak var {{ p.name }}Label: UILabel!
{% endfor %}

    override func awakeFromNib() {
        super.awakeFromNib()
    }

    func bindViewModel(_ viewModel: {{ model_name }}ViewModel?) {
        {% for p in properties %}
        {{ p.name }}Label.text = ""
        {% endfor %}
    }
}
