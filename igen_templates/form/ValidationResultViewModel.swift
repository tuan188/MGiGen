import Dto
import UIKit

struct ValidationResultViewModel {
    let validationResult: ValidationResult

    var backgroundColor: UIColor {
        switch validationResult {
        case .success:
            return UIColor.white
        case .failure:
            return UIColor.yellow
        }
    }

    var text: String {
        switch validationResult {
        case .success:
            return " "
        case .failure(let error):
            return error.localizedDescription
        }
    }
}