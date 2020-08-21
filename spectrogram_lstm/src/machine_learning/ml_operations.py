import tensorflow as tf

def ml_closure(model, loss_object, optimizer, train_loss, train_accuracy, val_loss, val_accuracy):
    epoch_ind = 0
    def run_epoch(train_dataset, val_dataset):
        nonlocal epoch_ind
        for test_x, labels in train_dataset:
            train_step(test_x, labels)

        for val_x, val_labels in val_dataset:
            val_step(val_x, val_labels)

        template = "Epoch: {}, Loss: {}, Accuracy: {}, Validation Loss: {}, Validation Accuracy: {}"
        print(template.format(epoch_ind + 1,
                              train_loss.result(),
                              train_accuracy.result() * 100,
                              val_loss.result(),
                              val_accuracy.result() * 100))

        # Reset metrics for next epoch
        train_loss.reset_states()
        train_accuracy.reset_states()
        val_loss.reset_states()
        val_accuracy.reset_states()

        epoch_ind += 1

    @tf.function
    def train_step(x, labels):
        with tf.GradientTape() as tape:
            predictions = model(x)
            loss_value = loss_object(labels, predictions)

        grads = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        train_loss(loss_value)
        train_accuracy(labels, predictions)

    @tf.function
    def val_step(x, labels):
        predictions = model(x)
        val_loss_value = loss_object(labels, predictions)

        val_loss(val_loss_value)
        val_accuracy(labels, predictions)

    return run_epoch, train_step, val_step