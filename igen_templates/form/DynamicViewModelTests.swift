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

    private let loadTrigger = PublishSubject<{{ name }}ViewModel.TriggerType>()
    private let {{ submit }}Trigger = PublishSubject<Void>()
    private let cancelTrigger = PublishSubject<Void>()
    private let dataTrigger = PublishSubject<{{ name }}ViewModel.DataType>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_name }}())

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            {{ submit }}Trigger: {{ submit }}Trigger.asDriverOnErrorJustComplete(),
            cancelTrigger: cancelTrigger.asDriverOnErrorJustComplete(),
            dataTrigger: dataTrigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

        {% for p in properties %}
        output.{{ p.name }}Validation.drive().disposed(by: disposeBag)
        {% endfor %}
        output.is{{ submit_title }}Enabled.drive().disposed(by: disposeBag)
        output.{{ submit }}.drive().disposed(by: disposeBag)
        output.cancel.drive().disposed(by: disposeBag)
        output.error.drive().disposed(by: disposeBag)
        output.isLoading.drive().disposed(by: disposeBag)
        output.cells.drive().disposed(by: disposeBag)
    }

    func test_loadTrigger_cells_need_reload() {
        // act
        loadTrigger.onNext(.load)

        let args = try? output.cells.toBlocking(timeout: 1).first()
        let cells = args?.0
        let needReload = args?.1

        // assert
        XCTAssertEqual(cells?.count, {{ properties|length }})
        XCTAssertEqual(needReload, true)
    }

    func test_loadTrigger_cells_no_need_reload() {
        // act
        loadTrigger.onNext(.endEditing)

        let args = try? output.cells.toBlocking(timeout: 1).first()
        let cells = args?.0
        let needReload = args?.1

        // assert
        XCTAssertEqual(cells?.count, {{ properties|length }})
        XCTAssertEqual(needReload, false)
    }

    func test_cancelTrigger_dismiss() {
        // act
        cancelTrigger.onNext(())

        // assert
        XCTAssert(navigator.dismissCalled)
    }

    {% for p in properties %}
    func test_dataTrigger_{{ model_variable }}_{{ p.name }}() {
        // act
        let {{ p.name }} = {{ p.type.mock_value }}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}))
        loadTrigger.onNext(.endEditing)
        let args = try? output.cells.toBlocking(timeout: 1).first()
        let cells = args?.0

        // assert
        if let dataType = cells?[{{ loop.index0 }}].dataType,
            case let {{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}) = dataType {
            XCTAssertEqual({{ p.name }}, {{ p.name }})
        } else {
            XCTFail()
        }
    }

    func test_dataTrigger_validate_{{ model_variable }}_{{ p.name }}() {
        // act
        let {{ p.name }} = {{ p.type.mock_value }}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.name }}))
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.validate{{ p.name_title }}Called)
    }

    {% endfor %}
    func test_loadTriggerInvoked_enable_{{ submit }}_byDefault() {
        // act
        loadTrigger.onNext(.load)
        let is{{ submit_title }}Enabled = try? output.is{{ submit_title }}Enabled.toBlocking(timeout: 1).first()

        // assert
        XCTAssertEqual(is{{ submit_title }}Enabled, true)
    }

    func test_{{ submit }}Trigger_not_{{ submit }}() {
        {% for p in properties %}
        useCase.validate{{ p.name_title }}ReturnValue = ValidationResult.invalid([TestError()])
        {% endfor %}

        // act
        {% for p in properties %}
        dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}({{ p.type.mock_value }}))
        {% endfor %}
        {{ submit }}Trigger.onNext(())
        let is{{ submit_title }}Enabled = try? output.is{{ submit_title }}Enabled.toBlocking(timeout: 1).first()

        // assert
        XCTAssertEqual(is{{ submit_title }}Enabled, false)
        XCTAssertFalse(useCase.{{ submit }}Called)
    }

    func test_{{ submit }}Trigger_{{ submit }}() {
        // act
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.{{ submit }}Called)
    }

    func test_{{ submit }}Trigger_{{ submit }}_fail_show_error() {
        // arrange
        let {{ submit }}ReturnValue = PublishSubject<Void>()
        useCase.{{ submit }}ReturnValue = {{ submit }}ReturnValue.asObserver()

        // act
        {{ submit }}Trigger.onNext(())
        {{ submit }}ReturnValue.onError(TestError())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssert(error is TestError)
    }

}