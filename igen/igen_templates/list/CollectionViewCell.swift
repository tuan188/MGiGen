import UIKit

final class {{model_name}}Cell: UICollectionViewCell, NibReusable {
{% for property in properties %}
    @IBOutlet weak var {{property.name}}Label: UILabel!
{% endfor %}

    override func awakeFromNib() {
        super.awakeFromNib()
    }

    func bindViewModel(_ viewModel: {{model_name}}ViewModel?) {
        if let viewModel = viewModel {
        {% for property in properties %}
            {{property.name}}Label.text = ""
        {% endfor %}
        } else {
        {% for property in properties %}
            {{property.name}}Label.text = ""
        {% endfor %}
        }
    }
}
