#!/bin/ash
DIRS=$(ls)
DATASTORE="datastore1"
# DIRS=$(ls | grep $VM_FOLDER_COMMON_NAME)

for dir in $DIRS; do
    if [[ -f $dir/*.vmx ]]; then
        vmkfstools -i /vmfs/volumes/$DATASTORE/scope-node-v3.1.7.vmdk -d thin $(pwd)/$dir/scope-node-v3.1.7.vmdk
        vim-cmd solo/registervm $(pwd)/$dir/$dir.vmx
    fi
done