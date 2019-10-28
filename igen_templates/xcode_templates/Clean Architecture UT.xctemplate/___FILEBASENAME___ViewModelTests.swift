//___FILEHEADER___

@testable import ___PROJECTNAME___
import XCTest
import RxSwift
import RxBlocking

final class ___VARIABLE_productName___ViewModelTests: XCTestCase {
    private var viewModel: ___VARIABLE_productName___ViewModel!
    private var navigator: ___VARIABLE_productName___NavigatorMock!
    private var useCase: ___VARIABLE_productName___UseCaseMock!
    
    private var input: ___VARIABLE_productName___ViewModel.Input!
    private var output: ___VARIABLE_productName___ViewModel.Output!
    
    private var disposeBag: DisposeBag!
    
    override func setUp() {
        super.setUp()
        navigator = ___VARIABLE_productName___NavigatorMock()
        useCase = ___VARIABLE_productName___UseCaseMock()
        viewModel = ___VARIABLE_productName___ViewModel(navigator: navigator, useCase: useCase)
        
        input = ___VARIABLE_productName___ViewModel.Input()
        output = viewModel.transform(input)
        
        disposeBag = DisposeBag()
    }
}
