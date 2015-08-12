angular.module('customControl', [])
    .directive('resourceform', [function () {
        return {
            restrict: 'E',
            scope: {
                resource: "="
            },
            link: function ($scope, element, attrs) {
                console.log($scope.resource);
                var resource = new $scope.resource;
                $scope.fields = resource.$options(function (value) {
                    $scope.fields = value.actions.POST;
                    $scope.headline = value.name.split(" ");
                    $scope.headline.pop();
                    $scope.headline = $scope.headline.join(" ");
                });
                $scope.obj = new $scope.resource;
            },
            templateUrl: "/static/common/resourceform.html",
            controller: function ($scope) {
                console.log($scope.resource);
            }
        };
    }])
    .directive('editable', ['$mdDialog', function ($mdDialog) {
        return {
            restrict: 'A', // only activate on element attribute
            scope: {
                res: '=',
                req: '='

            },
            link: function (scope, element, attrs) {
                if (scope.res.images[scope.req])
                    attrs.$set('ngSrc', scope.res.images[scope.req].full_size);
                function showAlert(ev) {
                    $mdDialog.show({
                        controller: DialogController,
                        templateUrl: '/static/common/imgcrop.html',
                        parent: angular.element(document.querySelector('body')),
                        targetEvent: ev,
                        clickOutsideToClose: true,
                        escapeToClose: true,

                    })
                        .then(function (image) {
                            scope.source = image;
                            attrs.$set('ngSrc', image);
                            scope.res.images[scope.req] = {
                                full_size: image
                            };
                            scope.res.$update();
                        }, function () {
                            $scope.alert = 'You cancelled the dialog.';
                        });
                };
                // Listen for change events to enable binding
                element.on('click', function () {
                    showAlert();
                });
            }
        };
    }]).
    directive('contenteditable', [function () {
        return {
            restrict: 'A', // only activate on element attribute
            scope: {
                res: '=',
                req: '='
            },
            link: function (scope, element, attrs) {
                element.html(scope.res[scope.req]);
                // Listen for change events to enable binding
                element.on('focus', function () {
                    element.text(element.html());
                    scope.res.$update();
                });
                element.on('blur', function () {
                    scope.res[scope.req] = element.text();
                    element.html(element.text());
                    scope.res.$update();
                });
            }
        };
    }]);

function DialogController($scope, $mdDialog) {
    $scope.hide = function () {
        $mdDialog.hide();
    };
    $scope.cancel = function () {
        $mdDialog.cancel();
    };
    $scope.confirm = function () {
        $mdDialog.hide($scope.myCroppedImage);
    };
    $scope.myImage = '';
    $scope.myCroppedImage = '';

    var handleFileSelect = function (evt) {
        var file = evt.currentTarget.files[0];
        var reader = new FileReader();
        reader.onload = function (evt) {
            $scope.$apply(function ($scope) {
                $scope.myImage = evt.target.result;
            });
        };
        reader.readAsDataURL(file);
    };
    angular.element(document).ready(function () {
            var temp = document.getElementById('fileInput');
            angular.element(temp).on('change', handleFileSelect);
        }
    );
}
