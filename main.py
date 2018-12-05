from spokenlang.features import *
import spokenlang.common as common
from spokenlang.folds import *
from spokenlang.model import *
import spokenlang.common as common

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate various features from audio samples.')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    parser.add_argument('--features', dest='features', action='store_true')
    parser.set_defaults(features=False)
    parser.add_argument('--folds', dest='folds', action='store_true')
    parser.set_defaults(folds=False)
    parser.add_argument('--model', dest='model', action='store_true')
    parser.set_defaults(model=False)
    parser.add_argument(
        '--test',
        dest='test',
        action='store_true',
        help='test the previously trained model against the test set')
    parser.set_defaults(test=False)

    args = parser.parse_args()

    if args.features:
        if args.debug:
            process_audio(os.path.join(common.DATASET_DIST, 'train'), debug=True)
        else:
            process_audio(os.path.join(common.DATASET_DIST, 'test'))
            process_audio(os.path.join(common.DATASET_DIST, 'train'))
    elif args.folds:

        '''generate_folds(
        os.path.join(common.DATASET_DIST, 'test'),
        '.fb.npz',
        output_dir='build/folds',
        group='test',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )
        generate_folds(
        os.path.join(common.DATASET_DIST, 'train'),
        '.fb.npz',
        output_dir='build/folds',
        group='train',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )'''
        generate_folds(
        os.path.join(common.DATASET_DIST, 'test'),
        '.mel.npz',
        output_dir='build/folds',
        group='test',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )
        generate_folds(
        os.path.join(common.DATASET_DIST, 'train'),
        '.mel.npz',
        output_dir='build/folds',
        group='train',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )
        generate_folds(
        os.path.join(common.DATASET_DIST, 'test'),
        '.chroma.npz',
        output_dir='build/folds',
        group='test',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )
        generate_folds(
        os.path.join(common.DATASET_DIST, 'train'),
        '.chroma.npz',
        output_dir='build/folds',
        group='train',
        input_shape=(WIDTH, FB_HEIGHT),
        normalize=normalize_fb,
        output_shape=(FB_HEIGHT, WIDTH, COLOR_DEPTH)
    )
    elif args.model:
        input_shape = (FB_HEIGHT, WIDTH, COLOR_DEPTH)
        if args.test:
            model = load_model('model.h5')

            input_shape = (FB_HEIGHT, WIDTH, COLOR_DEPTH)
            label_binarizer, clazzes = common.build_label_binarizer()

            test_labels, test_features, test_metadata = common.load_data(
                label_binarizer, 'build/folds', 'test', [1], input_shape)

            common.test(test_labels, test_features, test_metadata, model, clazzes)
        else:
            accuracies = []
            generator = common.train_generator(
                14, 'build/folds', input_shape, max_iterations=1)

            first = True
            for (train_labels,
                 train_features,
                 test_labels,
                 test_features,
                 test_metadata,
                 clazzes) in generator:

                # TODO reset tensorflow

                model = build_model(input_shape)
                if first:
                    model.summary()
                    first = False

                checkpoint = ModelCheckpoint(
                    'model.h5',
                    monitor='val_loss',
                    verbose=0,
                    save_best_only=True,
                    mode='min')

                earlystop = EarlyStopping(
                    monitor='val_loss',
                    min_delta=0,
                    patience=3,
                    verbose=0,
                    mode='auto')

                model.fit(
                    train_features,
                    train_labels,
                    epochs=20,
                    callbacks=[checkpoint, earlystop],
                    verbose=1,
                    validation_data=(test_features, test_labels),
                    batch_size=8)

                model = load_model('model.h5')

                scores = model.evaluate(test_features, test_labels, verbose=0)
                accuracy = scores[1]

                print('Accuracy:', accuracy)
                accuracies.append(accuracy)

                common.test(
                    test_labels,
                    test_features,
                    test_metadata,
                    model,
                    clazzes)

            accuracies = np.array(accuracies)

            print('\n## Summary\n')
            print("Mean: {mean}, Std {std}".format(
                mean=accuracies.mean(),
                std=accuracies.std()))    