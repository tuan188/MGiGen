@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_name }}())

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()
        
    {% for p in properties %}
        output.{{ p.name }}.drive().disposed(by: disposeBag)
    {% endfor %}
    }

    func test_loadTriggerInvoked_createCells() {
        // act
        loadTrigger.onNext(())
    {% for p in properties %}
        let {{ p.name }} = try? output.{{ p.name }}.toBlocking(timeout: 1).first()
    {% endfor %}
        
        // assert
        XCTAssert(true)
    }
}
