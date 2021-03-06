#coding=utf-8

import open3d as o3d
import numpy as np

realsense_pc = o3d.read_point_cloud("bpearl/ply/bpearl_trim.ply")
ouster_pc = o3d.read_point_cloud("velodyne/ply/velodyne_trim.ply")


# 为两个点云上上不同的颜色
realsense_pc.paint_uniform_color([0, 0.651, 0.929]) #target 为蓝色
ouster_pc.paint_uniform_color([1, 0.706, 0])    #source 为黄色

# 切记，将稠密点云当作src，将稀疏点云当作target
processed_source, outlier_index = o3d.geometry.radius_outlier_removal(realsense_pc,
                                              nb_points=16,
                                              radius=0.5)

processed_target, outlier_index = o3d.geometry.radius_outlier_removal(ouster_pc,
                                              nb_points=16,
                                              radius=0.5)

#o3d.geometry.radius_outlier_removal 这个函数是使用球体判断一个特例的函数，它需要
#两个参数：nb_points 和 radius。 它会给点云中的每个点画一个半径为 radius 的球体，如
#果在这个球体中其他的点的数量小于 nb_points, 这个算法会将这个点判断为特例，并删除。


threshold = 0.2  #移动范围的阀值
# src2target,using mechanical params
trans_init = np.asarray([[ 0.04329846, -0.01643883, 0.99456508, 0.2460109],
 [0.01637754, 1.00455503, 0.01501039, 0.07250645],
 [ -0.99983395, 0.01392359, 0.04123204, -0.18782889],
 [ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# trans_init = np.linalg.inv(trans_init)

#运行icp
reg_p2p = o3d.registration.registration_icp(
        processed_source, processed_target, threshold, trans_init,
        o3d.registration.TransformationEstimationPointToPoint())

#将我们的矩阵依照输出的变换矩阵进行变换
print(reg_p2p)
print("Transformation is:")
print(reg_p2p.transformation)
processed_source.transform(reg_p2p.transformation)

#创建一个 o3d.visualizer class
vis = o3d.visualization.Visualizer()
vis.create_window()

#将两个点云放入visualizer
vis.add_geometry(processed_source)
vis.add_geometry(processed_target)

#让visualizer渲染点云
vis.update_geometry()
vis.poll_events()
vis.update_renderer()

vis.run()





