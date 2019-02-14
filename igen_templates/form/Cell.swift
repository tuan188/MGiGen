import UIKit

final class {{ name }}{{ property.name_title }}Cell: UITableViewCell, NibReusable {
    
    {% if property.type.name == 'String' %}
    @IBOutlet weak var {{ property.name }}TextField: UITextField!
    @IBOutlet weak var {{ property.name }}ValidationLabel: UILabel!

    {% endif %}
    private(set) var disposeBag = DisposeBag()

    override func prepareForReuse() {
        super.prepareForReuse()
        disposeBag = DisposeBag()
    }
}