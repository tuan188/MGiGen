@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var disposeBag: DisposeBag!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)
        disposeBag = DisposeBag()

        input = {{ name }}ViewModel.Input()
        output = viewModel.transform(input)
    }
}
