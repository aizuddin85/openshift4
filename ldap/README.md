## Known Issue

1. Kubelet unable to start, complaining vm.overcommit_memory disabled.

When applying ```protectKernelDefaults: true```, make sure we have below sysctl applied to all nodes via MC.

```bash
vm.overcommit_memory=1
```

This is known behavior when ```protectKernelDefaults: true``` is set, it must have explicit sysctl to allow some kernel params to be set in order for kubelet able to start properly.

Corresponding github issue filed:  https://github.com/kubernetes/kubernetes/issues/66241
