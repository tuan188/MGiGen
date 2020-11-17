# igen - A code generator for iOS app

## Installation:
### Install using pip:
Open Terminal and run:

```
$ pip3 install igen
```

### Update:

```
$ pip3 install -U igen
```

or

```
$ pip3 uninstall igen
$ pip3 install igen --no-cache-dir
```

### Uninstall:

```
$ pip3 uninstall igen
```

## How to install pip3:
pip3 is already installed if you are using Python 3 (>=3.4)

In order to install Python 3, you need to install Homebrew, run the following command in Terminal:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python 3:

```
$ brew install python
```

## 1. Create Template:
### 1.1. Base Template:
The Base Template contains necessary files for a screen using the [Clean Architecture](https://github.com/tuan188/MGCleanArchitecture) pattern.

Open Terminal, navigate to the folder you want to save the files and run:

```
$ igen template base <Scene_Name> [--window]
```

#### Options:

`--window`: use UIWindow instead of UINavigationController in the Navigator.

The first time you use the `template` command, you need to enter your project information:

```
Enter project name: Your Project
Enter developer name: Your Name
Enter company name: Your Company
```

Later, if you want to update the information you can run:

```
$ igen config project
```

#### Example:

```
$ igen template base Login
```

Output:

```
Successfully created files:
    Login/LoginViewModel.swift
    Login/LoginNavigator.swift
    Login/LoginUseCase.swift
    Login/LoginViewController.swift
    Login/LoginAssembler.swift
    Login/Test/LoginViewModelTests.swift
    Login/Test/LoginUseCaseMock.swift
    Login/Test/LoginNavigatorMock.swift
    Login/Test/LoginViewControllerTests.swift
```

### 1.2. Skeleton Template:
To create a Clean Architecture skeleton project, run:

```
$ igen template skeleton <Folder_Name>
```

#### Example:
Run the following command in Terminal:

```
$ igen template skeleton DemoApp
```

Output:

```
Successfully created files:
    DemoApp/Podfile
    DemoApp/gitignore
    DemoApp/Localizable.strings
    DemoApp/pull_request_template.md
    DemoApp/swiftlint.yml
    DemoApp/DemoApp-Bridging-Header.h
    DemoApp/Sources/UnitTestViewController.swift
    DemoApp/Sources/AppDelegate.swift
    DemoApp/Sources/Assembler.swift
    DemoApp/Sources/Support/Utils.swift
    DemoApp/Sources/Support/Extensions/UIViewController+.swift
    DemoApp/Sources/Support/Extensions/UIViewController+Rx.swift
    DemoApp/Sources/Data/Gateways/GatewaysAssembler.swift
    DemoApp/Sources/Data/API/APIError.swift
    DemoApp/Sources/Data/API/APIService.swift
    DemoApp/Sources/Data/API/APIInput.swift
    DemoApp/Sources/Data/API/APIOutput.swift
    DemoApp/Sources/Config/APIUrls.swift
    DemoApp/Sources/Scenes/App/AppAssembler.swift
    DemoApp/Sources/Scenes/App/AppNavigator.swift
    DemoApp/Sources/Scenes/App/AppUseCase.swift
    DemoApp/Sources/Scenes/App/AppViewModel.swift
    DemoApp/Sources/Scenes/Storyboards/Storyboards.swift
```

### 1.3. List Template:
The List Template shows a list of objects in a UITableView or a UICollectionView.

Copy the model to the pasteboard (clipboard) then run:

```
$ igen template list <Scene_Name> [--section] [--collection] [--window] [--paging]
```

#### Options:

`--paging`: use pagination.

`--section`: show the list with header sections.

`--collection`: use UICollectionView instead of UITableView.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run:

```
$ igen template list ProductList
```

Output:

```
Successfully created files:
    ProductList/ProductListViewModel.swift
    ProductList/ProductItemViewModel.swift
    ProductList/ProductListNavigator.swift
    ProductList/ProductListUseCase.swift
    ProductList/ProductListViewController.swift
    ProductList/ProductCell.swift
    ProductList/ProductListAssembler.swift
    ProductList/Test/ProductListViewModelTests.swift
    ProductList/Test/ProductListUseCaseMock.swift
    ProductList/Test/ProductListNavigatorMock.swift
    ProductList/Test/ProductListViewControllerTests.swift
    ProductList/Test/ProductCellTests.swift
```

### 1.4. Detail Template:
The Detail Template shows details of an object in a UITableView.

Copy the model then run:

```
$ igen template detail <Scene_Name> [--static] [--window]
```

#### Options:

`--static`: display details of the object in a static UITableViewController.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run:

```
$ igen template detail ProductDetail
```

Output:

```
Successfully created files:
    ProductDetail/ProductDetailViewModel.swift
    ProductDetail/ProductDetailNavigator.swift
    ProductDetail/ProductDetailUseCase.swift
    ProductDetail/ProductDetailViewController.swift
    ProductDetail/ProductIdCell.swift
    ProductDetail/ProductNameCell.swift
    ProductDetail/ProductPriceCell.swift
    ProductDetail/ProductDetailAssembler.swift
    ProductDetail/Test/ProductDetailViewModelTests.swift
    ProductDetail/Test/ProductDetailUseCaseMock.swift
    ProductDetail/Test/ProductDetailNavigatorMock.swift
    ProductDetail/Test/ProductDetailViewControllerTests.swift
    ProductDetail/Test/ProductDetailCellsTests.swift
```

### 1.5. Form Input Template:
To create a form input template for a model, copy the model then run:

```
$ igen template form <Scene_Name> [--submit SUBMIT] [--dynamic] [--window]
```

#### Options:

`--submit`: set the name of the submit action.

`--dynamic`: use the dynamic form instead of the static form.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the model:

```swift
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then run:

```
$ igen template form CreateProduct --submit Create
```

Output:

```
Successfully created files:
    CreateProduct/CreateProductAssembler.swift
    CreateProduct/CreateProductNavigator.swift
    CreateProduct/CreateProductViewModel.swift
    CreateProduct/CreateProductUseCase.swift
    CreateProduct/CreateProductViewController.swift
    CreateProduct/Test/CreateProductUseCaseMock.swift
    CreateProduct/Test/CreateProductNavigatorMock.swift
    CreateProduct/Test/CreateProductViewModelTests.swift
    CreateProduct/Test/CreateProductViewControllerTests.swift
```

### 1.6. Setting Template:
To create a setting template, copy the setting enum then run:

```
$ igen template setting <Scene_Name> [--section] [--window]
```

#### Options:

`--section`: show the list with header sections.

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Copy the enum:

```swift
enum SettingMenu {
    case about
    case support
    case facebook
    case email
    case rating
}
```

then run:

```
$ igen template setting Setting
```

Output:

```
Successfully created files:
    Setting/SettingAssembler.swift
    Setting/SettingNavigator.swift
    Setting/SettingViewModel.swift
    Setting/SettingUseCase.swift
    Setting/SettingViewController.swift
    Setting/SettingMenuCell.swift
    Setting/Test/SettingUseCaseMock.swift
    Setting/Test/SettingNavigatorMock.swift
    Setting/Test/SettingViewModelTests.swift
    Setting/Test/SettingViewControllerTests.swift
    Setting/Test/SettingMenuCellTests.swift
```

### 1.7. Login template:
To create a login template, run:

```
$ igen template login <Scene_Name> [--window]
```

#### Options:

`--window`: use UIWindow instead of UINavigationController in the Navigator.

#### Example:
Run:

```
$ igen template login Login
```

Output:

```
Successfully created files:
    Login/LoginAssembler.swift
    Login/LoginNavigator.swift
    Login/LoginViewModel.swift
    Login/LoginUseCase.swift
    Login/LoginViewController.swift
    Login/LoginDto.swift
    Login/Test/LoginUseCaseMock.swift
    Login/Test/LoginNavigatorMock.swift
    Login/Test/LoginViewModelTests.swift
    Login/Test/LoginViewControllerTests.swift
```


## 2. Create a mock class for a protocol/function:
Copy the protocol/function then run:

```
$ igen mock [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:
Copy the protocol:

```swift
protocol ProductsNavigatorType {
    func toProducts()
    func toProductDetail(product: Product)
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate>
}
```

then run:

```
$ igen mock
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
final class ProductsNavigatorMock: ProductsNavigatorType {

    // MARK: - toProducts

    var toProductsCalled = false

    func toProducts() {
        toProductsCalled = true
    } 

    // MARK: - toProductDetail

    var toProductDetailCalled = false

    func toProductDetail(product: Product) {
        toProductDetailCalled = true
    } 

    // MARK: - toEditProduct

    var toEditProductCalled = false
    var toEditProductReturnValue = Driver<EditProductDelegate>.empty()

    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate> {
        toEditProductCalled = true
        return toEditProductReturnValue
    } 
}
```

## 3. Create unit tests for a view model:
Copy the view model then run:

```
$ igen test [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the view model:

```swift
struct LoginViewModel: ViewModel {
    struct Input {
        let usernameTrigger: Driver<String>
        let passwordTrigger: Driver<String>
        let loginTrigger: Driver<Void>
    }

    struct Output {
        @Property var usernameValidationMessage = ""
        @Property var passwordValidationMessage = ""
        @Property var isLoginEnabled = true
        @Property var isLoading = false
        @Property var error: Error?
    }
```

then run:

```
$ igen test
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
final class LoginViewModelTests: XCTestCase {
    private var viewModel: LoginViewModel!
    private var navigator: LoginNavigatorMock!
    private var useCase: LoginUseCaseMock!
    private var input: LoginViewModel.Input!
    private var output: LoginViewModel.Output!
    private var disposeBag: DisposeBag!

    // Triggers
    private let usernameTriggerTrigger = PublishSubject<String>()
    private let passwordTriggerTrigger = PublishSubject<String>()
    private let loginTriggerTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = LoginNavigatorMock()
        useCase = LoginUseCaseMock()
        viewModel = LoginViewModel(navigator: navigator, useCase: useCase)
        
        input = LoginViewModel.Input(
            usernameTrigger: usernameTrigger.asDriverOnErrorJustComplete(),
            passwordTrigger: passwordTrigger.asDriverOnErrorJustComplete(),
            loginTrigger: loginTrigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }
    
    func test_usernameTriggerTrigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

    func test_passwordTriggerTrigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

    func test_loginTriggerTrigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

}
```

## 4. Create an initialize method for a class/struct:
Copy the class/struct then run the command:

```
$ igen init [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the model:

```swift
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then run:

```
$ igen init
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
extension Product {
    init() {
        self.init(
            id: 0,
            name: "",
            price: 0.0
        )
    }
}
```

## 5. Create models from JSON:
Copy the json then run the command:

```
$ igen json <Model_Name> [-p]
```

#### Options:

`—-return-classes`: return classes instead of structs.

`-p`, `--print`: print the result.

#### Example:
Copy the json:

```json
{
    "id": 989,
    "content": "Hello world!",
    "is_read": false,
    "created_at": "2018-06-29T17:15:36+09:00"
}
```

then run:

```
$ igen json Notice
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

```swift
struct Notice {
    var id = 0
    var content = ""
    var isRead = false
    var createdAt = Date()
}

extension Notice: Then { }

extension Notice: Mappable {
    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
        id <- map["id"]
        content <- map["content"]
        isRead <- map["is_read"]
        createdAt <- (map["created_at"], DateTransform())
    }
}
```

## 6. File header command:
To update files’ headers, run:

```
$ igen header [--file-name] [--project] [--developer] [--created-date] [--copyright-year] [--company] <File_Paths>
```

#### Options:

`--file-name`: update file name.

`--project`: update project.

`--developer`: update developer.

`--created-date`: update created date.

`--copyright-year`: update copyright year.

`--company`: update company.

If you don’t set any options, the tool will update all header information base on its configuration file.

#### Example:

Update the company and the developer in AppDelegate’s header.

```
$ igen header AppDelegate.swift --company --developer
```

You can use wildcard as well:

Update all Swift files:

```
$ igen header *.swift
```

Update all Swift files in the Domain folder and its child folders (recursive) :

```
$ igen header Domain/**/*.swift
```

## 7. Configuration:
### 7.1. Configure the project information:
To update the project information, run:

```
$ igen config project [--global]
```

#### Options:

`--global`: global configuration.

### 7.2. View the configuration:
To view the configuration, run:

```
$ igen config [--global]
```

#### Options:

`--global`: global configuration.

### 7.3. Update a configuration:

```
$ igen config key value [--global] [--unset]
```

#### Options:
`--global`: global configuration.
`--unset`: delete a configuration.

#### Configure the project id:

```
$ igen config project.id <Project_ID>
```

Use the special value `@project` if you want to use the MD5 encoded project name as the project id.

```
$ igen config project.id @project
```

The project id will be used in file headers.

```swift
//
//  AppDelegate.swift
//  MGiGen (d18ea2a2902863a858af4f0e0911ed35)
//
//  Created by Tuan Truong on 3/27/19.
//  Copyright © 2019 Sun Asterisk. All rights reserved.
//
```

#### Configure the output path:

```
$ igen config output.path <Path>
```

Example:

Set the current working directory as the output path (relative path):

```
$ igen config output.path .
```

Set the desktop as the output path:

```
$ igen config output.path /Users/<Your_Name>/Desktop/
```

You can use a special value `@here`  to set the current working directory as the output path (absolute path):

```
$ igen config output.path @here
```

Other special values: `@desktop`, `@downloads`, `@documents`

### 7.4. View the available configurations:
To view the available configurations, run:

```
$ igen config keys
```

Output:

```
Available configuration keys:
    project.name
    project.developer
    project.company
    project.id
    output.path
```

### 7.5. Delete the configuration file:
To delete the configuration file, run:

```
$ igen config delete [--global]
```

#### Options:

`--global`: global configuration.

## 8. Install Xcode templates:

Install Clean Architecture templates for Xcode:

```
$ igen xcode install-templates
```

Uninstall templates:

```
$ igen xcode uninstall-templates
```

## 9. Other commands:

Run:

```
$ igen -h
```

## Links:
* [Clean Architecture](https://github.com/tuan188/MGCleanArchitecture)
